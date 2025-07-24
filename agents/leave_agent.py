"""
LeaveAgent: Answers leave balance queries from a local JSON file.
"""

from tools.leave_tools import leave_balance_tool
from langchain.llms import Ollama
from langchain.agents import initialize_agent, AgentType

def get_leave_agent():
    llm = Ollama(model="mistral")
    tools = [leave_balance_tool]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False,handle_parsing_errors=True)
