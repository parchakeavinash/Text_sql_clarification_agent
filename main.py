from app.agent.orchestrator import run_agent
from app.agent.conversation import resolve_clarification


def main():
    print("="*60)
    print("       E-COMMERCE TEXT-TO-SQL AGENT")
    print("="*60)

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ['exit','quite','q']:
            print('\nGoodbye!')
            break

        if not question:
            print('Please enter a question.')
            continue

        result = run_agent(
            question= question,
            provider='groq',
        )

        if result['status'] ==['invalid']:
            print('\nAgent:')
            print(result['message'])
            continue

        if result['status'] == 'needs_clarification':
            
            clarification_question = result['question']

            print('\nAgent:')
            print(clarification_question)

            # ask user for clarification
            user_answer = input("\nYou: ").strip()

            if not user_answer:
                print('Please provide a clarification.')
                continue

            # resolve clarification
            final_result = resolve_clarification(
                original_question=question,
                clarification_question=clarification_question,
                user_answer= user_answer,
                provider='groq'
            )

            if result['status'] == 'success':
                print("\n========== SQL ==========")
                print(result["sql"])

                print("\n========== EXPLANATION ==========")
                print(result["explanation"])

                print("\n========== TABLES USED ==========")
                print(result["tables_used"])

                print("\n========== DATABASE RESULT ==========")
                print(result["data"])

if __name__ =='__main__':
    main()