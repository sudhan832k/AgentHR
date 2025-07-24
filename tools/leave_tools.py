from langchain.tools import tool
import json
import os

def _load_leave_data(data_path="data/leave_data.json"):
    if not os.path.exists(data_path):
        return []
    with open(data_path, "r") as f:
        return json.load(f)

@tool
def leave_balance_tool(user: str) -> str:
    """Get all leave balances for a user as per the leave_data.json file."""
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

