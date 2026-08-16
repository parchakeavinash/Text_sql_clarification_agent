from app.agent.orchestrator import run_agent
from app.agent.conversation import resolve_clarification


def main():

    original_question = "Who is the best customer?"

    # -----------------------------------------
    # First interaction
    # -----------------------------------------

    result = run_agent(
        question=original_question,
        provider="groq",
    )

    print("\n========== AGENT RESPONSE ==========")
    print(result)

    # -----------------------------------------
    # Handle clarification
    # -----------------------------------------

    if result["status"] == "needs_clarification":

        clarification_question = result["question"]

        print("\n========== AGENT ASKS ==========")
        print(clarification_question)

        # Simulate user's answer
        user_answer = "The customer with the highest total revenue."

        print("\n========== USER ANSWER ==========")
        print(user_answer)

        # -----------------------------------------
        # Continue the conversation
        # -----------------------------------------

        final_result = resolve_clarification(
            original_question=original_question,
            clarification_question=clarification_question,
            user_answer=user_answer,
            provider="groq",
        )

        print("\n========== FINAL RESULT ==========")
        print(final_result)


if __name__ == "__main__":
    main()