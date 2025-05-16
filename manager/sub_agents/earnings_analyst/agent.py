import os
from dotenv import load_dotenv
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults
from datetime import datetime

load_dotenv()

# Check if the API key is loaded
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in environment variables")

APP_NAME = "financial_analysis_app"
USER_ID = "1234"
SESSION_ID = "session1234"

# Function to extract and process earnings information
def analyze_sec_filings(ticker: str) -> dict:
    """
    Find and analyze the latest 10-Q filing and earnings call transcript.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Analysis of SEC filings and earnings call
    """
    # This function calls the earnings_analyst agent
    # In a real implementation, this would connect to the agent
    # Here we're just showing the structure

    try:
        # In practice, the agent handles this internally
        return {
            "ticker": ticker,
            "filing_information": {
                "latest_10q_date": "2025-03-31",
                "latest_10q_quarter": "Q1 2025",
                "latest_earnings_call_date": "2025-04-15"
            },
            "financial_highlights": {
                "revenue": "$5.2B (up 15% YoY)",
                "eps": "$2.35 (GAAP), $2.47 (non-GAAP)",
                "gross_margin": "62.5%",
                "cash_position": "$12.8B",
                "debt": "$4.3B"
            },
            "management_commentary": [
                "Focused on AI integration across product lines",
                "Supply chain issues improving but still challenging",
                "Expanding market share in enterprise segment"
            ],
            "outlook_and_guidance": {
                "next_quarter_revenue": "$5.3B - $5.5B",
                "next_quarter_eps": "$2.40 - $2.50",
                "full_year_forecast": "Raised by 2%"
            },
            "risk_factors": [
                "Ongoing component shortages may impact production",
                "Increasing regulatory scrutiny in EU markets",
                "Foreign exchange headwinds expected to continue"
            ]
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e),
            "status": "failed"
        }

# Helper function for current date awareness
def get_current_time():
    """Get the current date and time.

    Returns:
        dict: Current date and time information
    """
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "year": now.year,
        "month": now.month,
        "day": now.day
    }


# Instantiate the LangChain tool
tavily_tool_instance = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

# Wrap it with LangchainTool for ADK
adk_tavily_tool = LangchainTool(tool=tavily_tool_instance)

# Create earnings agent focused specifically on 10-Q and earnings calls
earnings_analyst = LlmAgent(
    name="earnings_analyst",
    model="gemini-2.0-flash",
    description="An agent that analyzes SEC filings and earnings call transcripts",
    instruction="""
    You are a specialized financial analyst that focuses exclusively on two critical sources of company information:

    1. The most recent 10-Q quarterly SEC filing
    2. The latest earnings call transcript

    When given a company ticker symbol:

    FIRST, search for and analyze the latest 10-Q filing:
    - Use the adk_tavily_tool to search for "[TICKER] latest 10-Q SEC filing"
    - Extract and summarize key financial metrics including:
      * Revenue, net income, EPS (both GAAP and non-GAAP if available)
      * Year-over-year and quarter-over-quarter growth rates
      * Cash position and cash flow metrics
      * Debt levels and changes
      * Gross and operating margins
      * Any significant one-time items or adjustments

    SECOND, search for and analyze the latest earnings call transcript:
    - Use the adk_tavily_tool to search for "[TICKER] latest earnings call transcript"
    - Extract and summarize:
      * Management's key messages and themes
      * Guidance for future quarters (if provided)
      * Major strategic initiatives discussed
      * Notable analyst questions and management responses
      * Any significant challenges or opportunities mentioned

    Compile your findings into a structured analysis with these clearly labeled sections:
    1. Filing Information (date and quarter of latest 10-Q and earnings call)
    2. Financial Highlights (key metrics from 10-Q)
    3. Management Commentary (key points from earnings call)
    4. Outlook & Guidance (forward-looking statements)
    5. Risk Factors (important cautions from either source)

    Use the get_current_time tool to ensure you're referencing the most recent filings available.

    Focus exclusively on factual information from these two official sources. Do NOT include stock price data, 
    general news, or opinion pieces - that information will be provided by a separate agent.
    """,
    tools=[adk_tavily_tool, analyze_sec_filings, get_current_time],
    output_key='earnings_analysis'
)


