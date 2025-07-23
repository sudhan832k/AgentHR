from langchain.tools import tool

@tool
def onboarding_create_email(username: str) -> str:
    """Create an email for a new user."""
    return f"Created email for {username}"

@tool
def onboarding_assign_asset(username: str) -> str:
    """Assign an asset to a new user."""
    return f"Assigned laptop to {username}"

@tool
def onboarding_send_id_card(username: str) -> str:
    """Send an ID card to a new user."""
    return f"Sent ID card to {username}"
