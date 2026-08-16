from app.agent.orchestrator import run_agent
from app.agent.conversation import resolve_clarification


def main():
    print("=" * 60)
    print("       E-COMMERCE TEXT-TO-SQL AGENT")
    print("=" * 60)

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("\nGoodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        result = run_agent(
            question=question,
            provider="groq",
        )

        if result["status"] == "invalid":
            print("\nAgent:")
            print(result["message"])
            continue

        if result["status"] == "needs_clarification":

            clarification_question = result["question"]

            print("\nAgent:")
            print(clarification_question)

            user_answer = input("\nYou: ").strip()

            if not user_answer:
                print("Please provide a clarification.")
                continue

            final_result = resolve_clarification(
                original_question=question,
                clarification_question=clarification_question,
                user_answer=user_answer,
                provider="groq",
            )

            print("\nAgent:")
            print(final_result)

            continue

        print("\nAgent:")
        print(result)


if __name__ == "__main__":
    main()