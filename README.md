# Multi-Agent Financial Analysis System
A financial analysis toolkit built with Google ADK that combines multiple specialized agents to provide in-depth stock analysis.  It's not quite comprehensive yet in my mind.  But what I do like about Google ADK is the modularity.  So aside from improving on the prompt, you can spruce up the system by daisy-chain-ing more agents or dreaming up more tools which is something I intend to do in the future.   

## Example Output

![Financial Report Example](https://github.com/user-attachments/assets/5fabdde6-d80b-4959-b805-9c74f456dadd)

## Project Structure
```
multi-agent-example-finance/
│
├── manager/
│   ├── sub_agents/
│   │   ├── earnings_analyst/
│   │   │   ├── .env             # Environment variables for earnings analyst
│   │   │   ├── __init__.py      # Package initialization
│   │   │   └── agent.py         # Earnings analyst agent implementation
│   │   │
│   │   ├── finance_analyst/
│   │   │   ├── .env             # Environment variables for finance analyst
│   │   │   ├── __init__.py      # Package initialization
│   │   │   └── agent.py         # Finance analyst agent implementation
│   │   │
│   │   ├── news_analyst/        # News analysis agent
│   │   │
│   │   └── report_writer/       # Report generation agent
│   │
│   └── tools/                   # Shared tools and utilities
│   ├── .env                     # Environment variables for tools
│   ├── __init__.py              # Package initialization
│   └── agent.py                 # Shared agent functionality
│
└── .gitignore                   # Git ignore file
```

## Overview
This project implements a multi-agent system for comprehensive financial analysis, combining:
1. **Finance Analyst**: Retrieves key stock metrics, price data, and market information
2. **Earnings Analyst**: Analyzes SEC filings (10-Q) and earnings call transcripts
3. **News Analyst**: Gathers and summarizes recent news about the company
4. **Report Writer**: Combines all information into a comprehensive financial report

## Requirements
- Python 3.8+
- Google ADK
- API keys for:
  - Financial Modeling Prep (FMP) for stock data
  - Tavily for search functionality

## Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi-agent-financial-analysis.git
   cd multi-agent-example-finance
   ```

2. **Create and activate a virtual env**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create or update the .env files in each directory with the appropriate API keys

## Usage
### Option 1: Run interactive web interface
You can also run the agents interactively using Google ADK's built-in web interface
1. Navigate to your project directory
2. Launch the ADK web interface
```bash
adk web
```

### Option 2: Import in your code
```python
from manager.sub_agents.finance_analyst.agent import get_stock_data_fmp
from manager.sub_agents.earnings_analyst.agent import analyze_sec_filings
from manager.sub_agents.report_writer.agent import generate_financial_report

# Get stock data
stock_data = get_stock_data_fmp("AAPL")

# Get earnings data
earnings_data = analyze_sec_filings("AAPL")

# Generate a comprehensive report
report = generate_financial_report({
    "analyst_output": stock_data,
    "earnings_data": earnings_data
})

# Print the report
print(report["summary"])
print(report["report"])
```

## Features
- Comprehensive Financial Data: Stock prices, market metrics, and financial ratios
- SEC Filing Analysis: Extracts key information from quarterly reports
- Earnings Call Insights: Summarizes management commentary and guidance
- News Integration: Incorporates recent news and developments
- Structured Reports: Generates well-formatted financial reports with executive summaries

## API Keys
- Get a Financial Modeling Prep API key at financialmodelingprep.com
- Get a Tavily API key at tavily.com

## License
MIT

Note: This project is for educational and research purposes. Always conduct your own investment research and consult financial professionals before making investment decisions.
