"""
OnboardingAgent: LangChain tools for onboarding actions.
"""


from tools.onboarding_tools import onboarding_create_email, onboarding_assign_asset, onboarding_send_id_card
from langchain.llms import Ollama
from langchain.agents import initialize_agent, AgentType

def get_onboarding_agent():
    llm = Ollama(model="mistral")
    tools = [onboarding_create_email, onboarding_assign_asset, onboarding_send_id_card]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
