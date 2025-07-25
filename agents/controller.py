"""
Controller agent using LangChain's agent wrappers and Ollama (Mistral).
Connects onboarding, leave, and policy tools as true agents.
"""

from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
# from agents.onboarding_agent import get_onboarding_agent
from agents.leave_agent import get_leave_agent
from agents.policy_agent import get_policy_agent
from langchain.tools import tool, Tool
import json

# Wrap each sub-agent as a tool for the controller
# onboarding_agent = get_onboarding_agent()
leave_agent = get_leave_agent()
policy_agent = get_policy_agent()

# @tool
# def onboarding_agent_tool(query: str) -> str:
#     """Handle onboarding-related queries."""
#     return onboarding_agent.run(query)

def leave_agent_tool(query: str) -> str:
    result = leave_agent.invoke({"input": query})
    return result["output"] if isinstance(result, dict) and "output" in result else str(result)

def policy_agent_tool(query: str) -> str:
    result = policy_agent.invoke({"input": query})
    return result["output"] if isinstance(result, dict) and "output" in result else str(result)

llm = OllamaLLM(model="mistral")

with open("prompts.json") as f:
    prompts = json.load(f)
controller_tools = [ Tool(
        name="leave_agent_tool",
        func=leave_agent_tool,
        description=prompts["tool"]["leave_agent"]
    ),
    Tool(
        name="policy_agent_tool",
        func=policy_agent_tool,
        description=prompts["tool"]["policy_agent"]
    )
]
controller_prompt = prompts["controller_prompt"]
controller_agent = initialize_agent(controller_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False,handle_parsing_errors=True,agent_kwargs={"prefix": controller_prompt})

def handle_query(query: str) -> str:
    result = controller_agent.invoke({"input": query})
    response = result["output"] if isinstance(result, dict) and "output" in result else str(result)
    # Only return the 'Final Answer:' if present
    if "Final Answer:" in response:
        return response.split("Final Answer:", 1)[1].strip()
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
