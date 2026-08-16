from app.agent.generator import generate_sql
from app.database.connection import execute_query


def main():

    question = "How many orders were placed last month?"

    # 1. Generate SQL
    result = generate_sql(
        question=question,
        provider="groq",
    )

    print("\n========== GENERATED SQL ==========")
    print(result.sql)

    print("\n========== EXPLANATION ==========")
    print(result.explanation)

    print("\n========== TABLES USED ==========")
    print(result.tables_used)

    # 2. Execute SQL
    query_result = execute_query(result.sql)

    print("\n========== DATABASE RESULT ==========")
    print(query_result)


if __name__ == "__main__":
    main()