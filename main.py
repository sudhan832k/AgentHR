from agents.controller import handle_query
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio


from langchain.tools import Tool

def wrap_tool_for_agent(tool):
    async def wrapped_run(input_str: str):
        return await tool.arun({"args": {"query": input_str}})

    return Tool(
        name=tool.name,
        description=tool.description,
        func=wrapped_run,
        coroutine=wrapped_run,
        args_schema=None,  # Important: Remove args_schema to accept string
    )

async def main():
    client = MultiServerMCPClient({
        "controller_tools": {
            "transport": "streamable_http",
            "url": "http://localhost:8000/mcp"
        }
    })
    tools = await client.get_tools()
    wrapped_tools = [wrap_tool_for_agent(t) for t in tools]
    print(wrapped_tools)
    print("Welcome to AgentHR!")
    while True:
        query = input("Ask your HR question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        response = await handle_query(query, wrapped_tools)
        print(f"AgentHR: {response}")

if __name__ == "__main__":
    asyncio.run(main())