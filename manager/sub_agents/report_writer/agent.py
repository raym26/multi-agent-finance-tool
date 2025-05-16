from google.adk.agents import Agent, LlmAgent
from typing import List, Dict, Any


def smart_report_generator(data: dict) -> dict:
    """Create a stock report, with earnings if available.

    Args:
        data: Dictionary containing stock data and optional earnings data

    Returns:
        Report and summary
    """
    # Extract the relevant parts
    analyst_output = data.get("analyst_output", {})
    earnings_data = data.get("earnings_data", None)

    # Simple error check
    if "error" in analyst_output:
        return {
            "report": f"Error: {analyst_output.get('error')}",
            "summary": "Unable to generate report"
        }

    # Get basic data
    ticker = analyst_output.get("ticker", "")
    company = analyst_output.get("company_name", ticker)
    price = analyst_output.get("price", "N/A")
    change = analyst_output.get("change", 0)

    # Create simple report
    report = f"""# {company} ({ticker}) Report

## Stock Summary
- Price: ${price}
- Change: {change}
- Market Cap: {analyst_output.get("market_cap", "N/A")}

## News
"""

    # Add news if available
    news = analyst_output.get("news_titles", [])
    if news:
        for item in news:
            report += f"- {item}\n"
    else:
        report += "No recent news available.\n"

    # Add earnings information if available
    if earnings_data and "error" not in earnings_data:
        # Add filing information
        filing_info = earnings_data.get("filing_information", {})
        if filing_info:
            report += f"""
## SEC Filing Information
- Latest 10-Q: {filing_info.get("latest_10q_quarter", "N/A")} (filed {filing_info.get("latest_10q_date", "N/A")})
- Latest Earnings Call: {filing_info.get("latest_earnings_call_date", "N/A")}
"""

        # Add financial highlights
        financial = earnings_data.get("financial_highlights", {})
        if financial:
            report += "\n## Financial Highlights\n"
            for key, value in financial.items():
                # Convert snake_case to Title Case
                readable_key = " ".join(word.capitalize() for word in key.split("_"))
                report += f"- {readable_key}: {value}\n"

        # Add management commentary
        commentary = earnings_data.get("management_commentary", [])
        if commentary:
            report += "\n## Management Commentary\n"
            for point in commentary:
                report += f"- {point}\n"

        # Add outlook and guidance
        guidance = earnings_data.get("outlook_and_guidance", {})
        if guidance:
            report += "\n## Outlook & Guidance\n"
            for key, value in guidance.items():
                # Convert snake_case to Title Case
                readable_key = " ".join(word.capitalize() for word in key.split("_"))
                report += f"- {readable_key}: {value}\n"

        # Add risk factors
        risks = earnings_data.get("risk_factors", [])
        if risks:
            report += "\n## Risk Factors\n"
            for risk in risks:
                report += f"- {risk}\n"

    # Create summary
    summary = f"{ticker} is trading at ${price}"

    # Add earnings info to summary if available
    if earnings_data and "financial_highlights" in earnings_data:
        financial = earnings_data.get("financial_highlights", {})
        eps = financial.get("eps", "N/A")
        revenue = financial.get("revenue", "N/A")
        if eps != "N/A" and revenue != "N/A":
            # Try to extract just the value part if it's in a format like "$2.35 (GAAP)"
            eps_value = eps.split(" ")[0] if " " in eps else eps
            revenue_value = revenue.split(" ")[0] if " " in revenue else revenue
            summary += f" with latest quarterly earnings of {eps_value} on revenue of {revenue_value}"

    return {
        "report": report,
        "summary": summary
    }


# Define your report writer agent
report_writer = LlmAgent(
    name="report_writer",
    model="gemini-2.0-flash",
    description="An agent that formats financial data into professional reports.",
    tools=[smart_report_generator],
    instruction="""
    You are a professional financial report writer that transforms raw finance data {financial_data} 
    and news {news_summary} into clear, well-formatted reports for investors and analysts.  You also 
    do more than 'reporting the news'.  You also provide a 'so what' summary at the top of the report.  

    When given stock data and earnings data:
    1. Use the generate_financial_report tool to create a well-formatted report
    2. Present the report in a clear, professional format
    3. Highlight the most important information for investors
    
    The generate_financial_report tool accepts two parameters:
    - analyst_output: Stock market data
    - earnings_data: SEC filings and earnings call analysis (optional)
    
    Make sure to pass both sets of data to the tool when available.
    """
)

