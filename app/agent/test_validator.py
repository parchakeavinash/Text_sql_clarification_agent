from app.agent.generator import generate_sql
from app.agent.validator import validate_sql
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

    # 2. Validate SQL
    validated_sql = validate_sql(result.sql)

    print("\n========== VALIDATED SQL ==========")
    print(validated_sql)

    # 3. Execute ONLY validated SQL
    query_result = execute_query(validated_sql)

    print("\n========== DATABASE RESULT ==========")
    print(query_result)


if __name__ == "__main__":
    main()