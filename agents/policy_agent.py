"""
PolicyRAGAgent: Answers policy questions using FAISS and local embeddings.
"""

from tools.policy_tools import policy_query_tool
from model import getModel
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import json

with open("prompts.json") as f:
    prompts = json.load(f)

def get_policy_agent():
    llm = getModel()
    tools = [Tool(
        name="policy_query_tool",
        func=policy_query_tool,
        description=prompts["tool"]["policy_agent"]
    )]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False, handle_parsing_errors=True, agent_kwargs={"prefix": prompts["policy_agent_prompt"]})
