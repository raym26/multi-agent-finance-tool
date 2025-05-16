from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.finance_analyst.agent import finance_analyst
from .sub_agents.report_writer.agent import report_writer
from .sub_agents.earnings_analyst.agent import earnings_analyst
from .tools.tools import get_current_time

root_agent = SequentialAgent(
    name="manager",
    #model="gemini-2.0-flash",
    description="Manager agent",
    sub_agents=[finance_analyst, news_analyst, earnings_analyst,report_writer],
)