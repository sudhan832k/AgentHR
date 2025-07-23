from langchain.tools import tool

@tool
def policy_query_tool(query: str) -> str:
    """Answer a policy question using the local policy document."""
    # Dummy: In real code, retrieve relevant chunk and use LLM to answer
    return "Policy answer (dummy): Please refer to the leave policy document."
