from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
import json
from model import get_gemini

with open("prompts.json") as f:
    prompts = json.load(f)

async def handle_query(query: str, tools: list) -> str:
    print("Controller received query:", query)

    # prompt = PromptTemplate(
    #     input_variables=["input"],
    #     template=prompts["controller"],
    # )

    controller_agent = initialize_agent(
        tools,
        llm=get_gemini(),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={"system_message": prompts["controller"]},
        handle_parsing_errors=True,
        iterative_steps=False,
         
    )

    result = await controller_agent.ainvoke({"input": query})

    if "Final Answer:" in result:
        return result.split("Final Answer:", 1)[1].strip()
    return result
