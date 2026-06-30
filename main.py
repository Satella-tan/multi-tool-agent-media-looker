from agent.core import run_agent

def main():
    print("Multi-Tool AI Agent (Terminal Mode)")
    print("-----------------------------------")

    question = input('Ask a basic math operation, google search, or about your media library:')
    print(f"Asking: '{question}'")

    response = run_agent(question)
    print("\nAgent Response:")
    print(response)

if __name__ == "__main__":
    main()
