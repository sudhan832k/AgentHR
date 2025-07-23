"""
Controller agent using LangChain's agent wrappers and Ollama (Mistral).
Connects onboarding, leave, and policy tools as true agents.
"""

from langchain.llms import Ollama
from langchain.agents import initialize_agent, AgentType
# from agents.onboarding_agent import get_onboarding_agent
from agents.leave_agent import get_leave_agent
from agents.policy_agent import get_policy_agent
from langchain.tools import tool

# Wrap each sub-agent as a tool for the controller
# onboarding_agent = get_onboarding_agent()
leave_agent = get_leave_agent()
policy_agent = get_policy_agent()

# @tool
# def onboarding_agent_tool(query: str) -> str:
#     """Handle onboarding-related queries."""
#     return onboarding_agent.run(query)

@tool
def leave_agent_tool(query: str) -> str:
    """
    Use this tool to answer questions about a specific user's personal leave balance, such as 'How many sick leaves do I have left?' or 'What is my remaining casual leave?'.
    Do not use for general company leave policy questions.
    """
    return leave_agent.run(query)

@tool
def policy_agent_tool(query: str) -> str:
    """
    Use this tool to answer general questions about company leave policy, rules, types of leave, or eligibility (e.g., 'What is the sick leave policy?', 'How many types of leave are there?').
    Do not use for user-specific leave balance questions.
    """
    return policy_agent.run(query)

llm = Ollama(model="mistral")
controller_tools = [leave_agent_tool, policy_agent_tool]
controller_agent = initialize_agent(controller_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def handle_query(query: str) -> str:
    response = controller_agent.run(query)
    fallback_phrases = [
        "I'm not sure",
        "I do not know",
        "I don't know",
        "Sorry",
        "cannot answer",
        "no tool"
    ]
    if any(phrase.lower() in response.lower() for phrase in fallback_phrases):
        return "Sorry, I can only answer questions about your personal leave or company leave policy."
    return response
