"""
PolicyRAGAgent: Answers policy questions using FAISS and local embeddings.
"""

from tools.policy_tools import policy_query_tool
from langchain.llms import Ollama
from langchain.agents import initialize_agent, AgentType

def get_policy_agent():
    llm = Ollama(model="mistral")
    tools = [policy_query_tool]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
