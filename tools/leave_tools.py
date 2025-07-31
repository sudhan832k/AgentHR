from langchain.tools import tool
import json
import os

def _load_leave_data(data_path="data/leave_data.json"):
    if not os.path.exists(data_path):
        return []
    with open(data_path, "r") as f:
        return json.load(f)

def leave_balance_tool(user: str, leavetype: optional[str] = None) -> str:
    print("[INFO] leave_balance_tool invoked.", user, leavetype)

    # Validate input
    if not user or not user.strip():
        return "[ERROR] No user name provided. Please pass a valid user name."

    user = user.strip().lower()  # Normalize input

    leave_data = _load_leave_data()

    # Search user case-insensitively
    user_obj = next((u for u in leave_data if u.get("name", "").lower() == user), None)

    if not user_obj:
        return f"[INFO] No leave data found for user '{user}'."

    if leavetype:
        leavetype = leavetype.lower()
        if leavetype in user_obj:
            info = user_obj[leavetype]
            balance = info.get("balance", 0)
            used = info.get("used", 0)
            return f"{leavetype.capitalize()} Leave for {user_obj['name']}: {balance} (used: {used})"
        else:
            return f"{leavetype.capitalize()} leave data not found for {user_obj['name']}."
    else:
        # Return all available leave types
        balances = []
        for leave_type, info in user_obj.items():
            if leave_type == "name":
                continue
            if isinstance(info, dict):
                balance = info.get("balance", 0)
                used = info.get("used", 0)
                balances.append(f"{leave_type.capitalize()}: {balance} (used: {used})")
        return f"Leave balances for {user_obj['name']}: {', '.join(balances)}."
