"""
Main entry point for the multi-agent HR system.
Provides a CLI and Streamlit UI for user interaction.
"""


from agents.controller import handle_query

def main():
    print("Welcome to AgentHR!")
    while True:
        query = input("Ask your HR question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        response = handle_query(query)
        print(f"AgentHR: {response}")

if __name__ == "__main__":
    main()