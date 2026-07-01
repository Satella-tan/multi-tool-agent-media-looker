from agent.core import run_agent

def main():
    print("-----------------------------------")
    print("Multi-Tool AI Agent (Terminal Mode)")
    print("-----------------------------------")

    while True:
        try:
            question = input('\nAsk a basic math operation, google search, or about your media library (or type "exit" to quit): ')
            if question.strip().lower() == "exit":
                print("Goodbye!")
                break
            if not question.strip():
                continue

            print(f"Asking: '{question}'")
            # For now run_agent might return a dict after fastapi implementation so we will support both formats
            res = run_agent(question)

            # Print response based on whether it is a dict (fastapi) or string (old cli)
            if isinstance(res, dict):
                print("\nAgent Response:")
                print(res["response"])
                if res["tools_used"]:
                    print(f"[Tools used: {', '.join(res['tools_used'])}]")
            else:
                print("\nAgent Response:")
                print(res)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
