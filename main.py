from app.agent.generator import generate_sql
from app.agent.prompt import SYSTEM_PROMPT
from app.agent.validator import validate_sql
from app.database.connection import execute_query


def main():
    print("="*50)
    print("      Text-to-sql-Agent")
    print("="*50)

    question = input("\nAsk a question: ").strip()

    if not question:
        print("Please enter a question")
        return 

    try:
        #generate sql
        sql = generate_sql(
            question=question,
        )
         # 2. Validate SQL
        validated_sql = validate_sql(result.sql)


        print("\n Generating sql query...")

        print("="*50)
        print(sql)

        #execut sql query
        print("\n Executing query...")

        result = execute_query(validated_sql)

        #step 3 display result
        print("\nResult")
        print("="*50)

        if not result:
            print("no result found..")
            return

        # for row in result:
        #     print(row)
        print(result)
    except Exception as e:
        print("\nError.")
        print(e)



if __name__ =="__main__":
    main()