from mcp.server.fastmcp import FastMCP
import json

with open("prompts.json") as f:
    prompts = json.load(f)

mcp = FastMCP("controller_tools")

@mcp.tool(name="leave_balance_tool", description=prompts["tool"]["leave_agent"])
def leave_balance_tool(args: dict) -> str:
    user = args.get("user")
    if not user:
        return "[ERROR] No user provided."
    from tools.leave_tools import leave_balance_tool as internal_tool
    return internal_tool(user)

@mcp.tool(name="policy_agent_tool", description=prompts["tool"]["policy_agent"])
def policy_query_tool(args: dict) -> str:
    print("[INFO] policy_query_tool invoked with args:", args)
    query = args.get("query")
    if not query:
        return "[ERROR] No query provided."
    from tools.policy_tools import policy_query_tool as internal_tool
    return internal_tool(query)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")