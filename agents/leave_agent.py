"""
LeaveAgent: Answers leave balance queries from a local JSON file.
"""

from tools.leave_tools import leave_balance_tool
from model import get_gemini
from langchain.agents import initialize_agent, AgentType
import json
from langchain.tools import Tool


with open("prompts.json") as f:
    prompts = json.load(f)

def get_leave_agent():
    llm = get_gemini()
    tools = [Tool(
        name="leave_balance_tool",
        func=leave_balance_tool,
        description=prompts["tool"]["leave_agent"]
    )]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False,handle_parsing_errors=True, agent_kwargs={"prefix": prompts["leave_agent_prompt"]})