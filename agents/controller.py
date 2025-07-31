from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
import json
from model import getModel
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

with open("prompts.json") as f:
    prompts = json.load(f)


async def handle_query(query: str, tools: list) -> str:

    controller_agent = initialize_agent(
        tools,
        llm=getModel(),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={"system_message":prompts["controller"]},
        handle_parsing_errors=True,
        iterative_steps=False,  
    )

    result = await controller_agent.ainvoke({"input": query})

    if "Final Answer:" in result:
        return result.split("Final Answer:", 1)[1].strip()
    return result
