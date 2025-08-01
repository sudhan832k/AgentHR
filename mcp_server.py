from mcp.server.fastmcp import FastMCP
import json

from agents.leave_agent import get_leave_agent
from agents.policy_agent import get_policy_agent

# Load prompt descriptions
with open("prompts.json") as f:
    prompts = json.load(f)

mcp = FastMCP("controller_tools")

@mcp.tool(name="subagent_leave_balance_tool", description="Use for personal leave balance queries. Input should be the user's full query.")
def subagent_leave_balance_tool(args: dict) -> str:
    print("[INFO] subagent_leave_balance_tool invoked with args:", args)
    result = get_leave_agent().invoke({"user":"Selvasudhan"})
    if isinstance(result, dict):
        return result.get("output", str(result))  # fallback: convert entire dict to string
    return str(result)

@mcp.tool(name="subagent_policy_query_tool", description="Use for general HR leave policy questions. Input should be the user's full query as a string.")
def subagent_policy_query_tool(args: dict) -> str:
    print("[INFO] subagent_policy_query_tool invoked with args:", args)
    result = get_policy_agent().invoke({"input": {"query": args["query"]}})
    print("[INFO] subagent_policy_query_tool result:", result)
    if isinstance(result, dict):
        return result.get("output", str(result))  # fallback: convert entire dict to string
    return str(result)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")  # or "streamable-sub http"