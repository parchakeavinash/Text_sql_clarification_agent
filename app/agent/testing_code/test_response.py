from app.agent.response import generate_natural_language_response


def run_response():

    question = "Who has spent the most money?"

    sql = """
    SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
           SUM(o.total_amount) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, customer_name
    ORDER BY total_spent DESC
    LIMIT 1;
    """

    result = [
        {
            "customer_name": "Candace Cruz",
            "total_spent": 12543.50,
        }
    ]

    response = generate_natural_language_response(
        question=question,
        sql=sql,
        result=result,
        provider="groq",
    )

    print("\n================================")
    print("QUESTION:")
    print(question)

    print("\nDATABASE RESULT:")
    print(result)

    print("\nNATURAL LANGUAGE RESPONSE:")
    print(response)


def main():
    run_response()


if __name__ == "__main__":
    main()