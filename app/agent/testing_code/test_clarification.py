from app.agent.clarification import classify_question


def test_question(question: str):

    result = classify_question(
        question=question,
        provider="groq",
    )

    print("\n================================")
    print("QUESTION:")
    print(question)

    print("\nCLASSIFICATION:")
    print(result.classification)

    print("\nREASONING:")
    print(result.reasoning)

    print("\nCLARIFICATION:")
    print(result.clarification_question)


def main():

    test_question(
        "Who is the best customer?"
    )


if __name__ == "__main__":
    main()
    