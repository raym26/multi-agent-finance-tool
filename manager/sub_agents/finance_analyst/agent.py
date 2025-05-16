from datetime import datetime
from google.adk.agents import Agent
import pandas as pd
from datetime import datetime, timedelta

import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any


def get_stock_data(ticker: str) -> Dict[str, Any]:
    """
    Get comprehensive stock data including price information and recent news.

    Args:
        ticker (str): Stock ticker symbol (e.g., "NVDA", "AAPL")

    Returns:
        dict: Dictionary containing financial data and news summary
    """
    try:
        # Get stock info
        stock = yf.Ticker(ticker)

        # Get current data
        info = stock.info
        history = stock.history(period="2d")

        # Calculate day change
        if not history.empty and len(history) > 1:
            current_price = history["Close"].iloc[-1]
            prev_close = history["Close"].iloc[-2]
            day_change = current_price - prev_close
            day_change_percent = (day_change / prev_close) * 100
        else:
            current_price = info.get("currentPrice", None)
            prev_close = info.get("previousClose", None)
            day_change = current_price - prev_close if current_price and prev_close else None
            day_change_percent = ((
                                              current_price - prev_close) / prev_close) * 100 if current_price and prev_close else None

        # Build finance data dictionary
        finance_data = {
            "ticker": ticker,
            "company_name": info.get("shortName", ticker),
            "current_price": current_price,
            "prev_close": prev_close,
            "day_change": day_change,
            "day_change_percent": day_change_percent,
            "volume": info.get("volume", None),
            "market_cap": info.get("marketCap", None),
            "pe_ratio": info.get("trailingPE", None),
            "dividend_yield": info.get("dividendYield", None) * 100 if info.get("dividendYield") else None,
            "52w_high": info.get("fiftyTwoWeekHigh", None),
            "52w_low": info.get("fiftyTwoWeekLow", None)
        }

        # Get news
        news_summary = "No recent news available."
        news_items = []

        try:
            news = stock.news
            if news:
                news_items = []
                news_summary = f"Here's a summary of recent news regarding {ticker}:\n"

                for i, item in enumerate(news[:5]):
                    news_date = datetime.fromtimestamp(item.get('providerPublishTime', 0))
                    formatted_date = news_date.strftime('%Y-%m-%d')

                    title = item.get('title', '')
                    publisher = item.get('publisher', '')

                    news_summary += f"* **{title}** ({publisher}, {formatted_date})\n"

                    news_items.append({
                        "title": title,
                        "publisher": publisher,
                        "date": formatted_date,
                        "summary": item.get('summary', '')
                    })
        except:
            pass

        return {
            "finance_data": finance_data,
            "news_summary": news_summary
        }

    except Exception as e:
        return {
            "finance_data": {"ticker": ticker, "error": str(e)},
            "news_summary": f"Error retrieving data for {ticker}: {str(e)}"
        }


import requests
import json

import requests
from datetime import datetime
import time
import os
from dotenv import load_dotenv
load_dotenv()


def get_stock_data_fmp(ticker: str) -> dict:
    """Get stock data for a ticker.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Stock data and news
    """
    # Get API key
    api_key = os.getenv("FMP_API_KEY")

    # Debug log
    print(f"Function called with ticker: {ticker}")
    print(f"API key exists: {api_key is not None}")

    # Basic error check
    if not api_key:
        return {"error": "API key not found in environment"}

    try:
        # Make API calls
        quote_url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
        news_url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={ticker}&limit=5&apikey={api_key}"

        print(f"Calling quote URL: {quote_url.replace(api_key, 'HIDDEN')}")
        quote_response = requests.get(quote_url)
        print(f"Quote response status: {quote_response.status_code}")

        if quote_response.status_code == 200:
            quote = quote_response.json()
            print(f"Quote data received: {len(quote) if isinstance(quote, list) else 'Not a list'}")
            if isinstance(quote, list) and len(quote) > 0:
                print(f"First quote item keys: {list(quote[0].keys())}")

            print(f"Calling news URL: {news_url.replace(api_key, 'HIDDEN')}")
            news_response = requests.get(news_url)
            print(f"News response status: {news_response.status_code}")

            if news_response.status_code == 200:
                news = news_response.json()
                print(f"News items received: {len(news) if isinstance(news, list) else 'Not a list'}")
            else:
                news = []

            # Check if we got data
            if not quote or len(quote) == 0:
                print(f"No quote data found for ticker {ticker}")
                return {"error": f"No data found for ticker {ticker}"}

            # Format response - make a very simple structure
            data = {
                "success": True,
                "ticker": ticker,
                "price": quote[0].get("price"),
                "company_name": quote[0].get("name", ticker),
                "change": quote[0].get("change"),
                "change_percent": quote[0].get("changesPercentage"),
                "market_cap": quote[0].get("marketCap"),
                "news_count": len(news),
                "news_titles": [item.get("title") for item in news[:3]] if news else []
            }

            print(f"Returning success data: {json.dumps(data)[:200]}...")
            return data
        else:
            error_msg = f"API returned status code {quote_response.status_code}"
            print(error_msg)
            return {"error": error_msg}

    except Exception as e:
        error_msg = f"Exception: {str(e)}"
        print(error_msg)
        return {"error": error_msg}


# Updated stock_analyst agent
# Create the agent with improved handling
finance_analyst = Agent(
    name="finance_analyst",
    model="gemini-2.0-flash",
    description="Stock information lookup",
    tools=[get_stock_data_fmp],
    output_key="financial_data",
    instruction="""
    You are a helpful stock market assistant that looks up current stock information.

    When asked about a stock:
    1. Call the get_stock_data_fmp tool with the ticker symbol
    2. Check if the response contains an "error" field:
       - If it does, politely inform the user about the error and suggest they check the ticker symbol
       - If it doesn't, provide the stock information in a clear format

    For successful responses, include:
    - Current price
    - Company name
    - Price change information
    - Recent news headlines (if available)

    Always check the structure of the response carefully before trying to access any fields.
    Sample successful response structure:
    {
      "success": true,
      "ticker": "AAPL",
      "price": 170.25,
      "company_name": "Apple Inc",
      "change": 2.35,
      "change_percent": 1.2,
      "market_cap": 2500000000000,
      "news_count": 5,
      "news_titles": ["Title 1", "Title 2", "Title 3"]
    }

    Sample error response structure:
    {
      "error": "Error message here"
    }
    """
)



