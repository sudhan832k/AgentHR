controller.py"""
Controller agent using LangChain's agent wrappers and Ollama (Mistral).
Connects onboarding, leave, and policy tools as true agents.
"""

from model import get_gemini
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

llm = get_gemini()

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
controller_agent = initialize_agent(controller_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,handle_parsing_errors=True,agent_kwargs={"prefix": controller_prompt})

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


    leave_agent_prompt.py"""
LeaveAgent: Answers leave balance queries from a local JSON file.
"""

from tools.leave_tools import leave_balance_tool
from model import get_gemini
from langchain.agents import initialize_agent, AgentType
import json
from langchain.tools import Tool


with open("prompts.json") as f:
    prompts = json.load(f)

def get_leave_agent():
    llm = get_gemini()
    tools = [Tool(
        name="leave_balance_tool",
        func=leave_balance_tool,
        description=prompts["tool"]["leave_agent"]
    )]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False,handle_parsing_errors=True, agent_kwargs={"prefix": prompts["leave_agent_prompt"]})

policy_agent.py
"""
PolicyRAGAgent: Answers policy questions using FAISS and local embeddings.
"""

from tools.policy_tools import policy_query_tool
from model import get_gemini
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import json

with open("prompts.json") as f:
    prompts = json.load(f)

def get_policy_agent():
    llm = get_gemini()
    tools = [Tool(
        name="policy_query_tool",
        func=policy_query_tool,
        description=prompts["tool"]["policy_agent"]
    )]
    return initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False, handle_parsing_errors=True, agent_kwargs={"prefix": prompts["policy_agent_prompt"]})
toolsfrom langchain.tools import tool
import json
import os

def _load_leave_data(data_path="data/leave_data.json"):
    if not os.path.exists(data_path):
        return []
    with open(data_path, "r") as f:
        return json.load(f)

def leave_balance_tool(user: str) -> str:
    print("[INFO] leave_balance_tool invoked.")
    # Validate input
    if not user or not user.strip():
        return "[ERROR] No user name provided. Please pass a valid user name."

    user = user.strip().lower()  # Normalize input

    leave_data = _load_leave_data()

    # Search user case-insensitively
    user_obj = next((u for u in leave_data if u.get("name", "").lower() == user), None)

    if not user_obj:
        return f"[INFO] No leave data found for user '{user}'."

    # Collect leave balances
    balances = []
    for leave_type, info in user_obj.items():
        if leave_type == "name":
            continue
        if isinstance(info, dict):
            balance = info.get("balance", 0)
            used = info.get("used", 0)
            balances.append(f"{leave_type}: {balance} (used: {used})")

    return f"Leave balances for {user_obj['name']}: {', '.join(balances)}."


import os
from langchain.tools import tool
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from model import get_gemini

def policy_query_tool(query: str) -> str:
    print("[INFO] policy_query_tool invoked.")
    # Path to the FAISS index
    faiss_index_path = os.path.join(os.path.dirname(__file__), '../data/policy_faiss_index')

    # Only load FAISS vectorstore; do not create it here
    if not os.path.exists(faiss_index_path):
        return "Policy vectorstore not found. Please run policy_vectorstore.py to create it first."
    db = FAISS.load_local(faiss_index_path, OllamaEmbeddings(model="mistral"), allow_dangerous_deserialization=True)

    # Retrieve relevant chunks
    print("[INFO] Performing similarity search.")
    relevant_docs = db.similarity_search(query, k=3)
    print(f"[INFO] Found {len(relevant_docs)} relevant documents.")
    context = "\n".join([doc.page_content for doc in relevant_docs])

    # Use LLM to answer based on context
    llm = get_gemini()
    prompt = f"Answer the following question using only the context below. If the answer is not in the context, say you don't know.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    answer = llm.invoke(prompt)
    return answer.strip()
prompt.json
{
    "controller_prompt": "You are an intelligent HR assistant responsible for answering HR leave-related queries by selecting and calling exactly one tool at a time.\n\nYou have access to the following tools:\n\n1. `leave_agent_tool`: Use only for questions about a specific user's personal leave balance (e.g., \"How many sick leaves do I have left?\", \"Vinoth's casual leave?\").\n\n2. `policy_agent_tool`: Use only for general leave policy questions (e.g., \"What is the sick leave policy?\", \"What types of leave are available?\").\n\nImportant rules:\n- NEVER return more than one Action.\n- NEVER combine Action and Final Answer together.\n- ALWAYS output either a single Action OR a Final Answer.\n- If the user asks a personal leave question without a name (e.g., 'my leave'), still call `leave_agent_tool` — it will handle name collection.\n\nYour job is to always pick the right tool and call it correctly.\n\n### Examples ###\n\nQuestion: How many types of leave are there?\nThought: This is a general policy question.\nAction: policy_agent_tool\nAction Input: What types of leave are there?\n\nQuestion: How many casual leaves do I have left?\nThought: This is a personal leave balance question.\nAction: leave_agent_tool\nAction Input: How many casual leaves do I have left?\n\nQuestion: What is the eligibility for paternity leave?\nThought: This is a policy-related question.\nAction: policy_agent_tool\nAction Input: What is the eligibility for paternity leave?\n\nQuestion: How many leaves has Vinoth taken?\nThought: This is a personal leave balance question.\nAction: leave_agent_tool\nAction Input: How many leaves has Vinoth taken?",
    "leave_agent_prompt": "You are an HR assistant that helps employees check their personal leave balances using the leave_balance_tool.\n\nWhenever a user asks about leave (e.g., sick or casual leave), you must extract the person's name from the input.\n\nIf the name is not mentioned (e.g., user says 'my leave' or 'How many leaves do I have?'), **do not proceed** — instead, ask the user to provide their name.\n\nOnly use the leave_balance_tool if the name is available. Do not assume or guess any default name.\n\nTreat phrases like \"I\", \"my\", or \"me\" as requiring clarification — ask the user to provide their name explicitly.\n\nExamples:\n- 'How many sick leaves do I have?' → ask the user to provide their name\n- 'Check leave balance for Vinoth' → call leave_balance_tool with 'Vinoth'\n- 'What's Arjun’s casual leave?' → call leave_balance_tool with 'Arjun'",
    "policy_agent_prompt": "You are an HR policy expert. You assist employees by answering questions related to company leave policies.\n\nYour responsibilities include:\n- Explaining the different types of leaves (e.g., sick leave, casual leave, parental leave, etc.)\n- Providing details on eligibility criteria, limits, and applicable conditions for various leave types.\n- Clarifying how many days each leave type allows.\n\nYou must not give personal leave balances (e.g., 'How many sick leaves do I have?') or answer questions like 'What is my remaining casual leave?'.\n\nIf you are unsure of the exact policy, reply with: 'Please check with HR for more details.'",
    "tool": {
        "leave_agent": "Use this tool to answer questions about a specific user's personal leave balance.\nExamples:\n- 'How many sick leaves do I have left?'\n- 'What is my remaining casual leave?'\n- 'How many leaves has Vinoth used?'\n\n!Do NOT use this tool for general leave policy questions like 'What is the sick leave policy?'",
        "policy_agent": "Use this tool to answer general questions about company leave policy, rules, types of leave, or eligibility.\nExamples:\n- 'What is the sick leave policy?'\n- 'How many types of leave are there?'\n- 'Who is eligible for paternity leave?'\n\n!Do NOT use this tool for personal leave balance questions like 'How many sick leaves do I have?'"
    }
}