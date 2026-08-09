from app.database.connection import execute_query


result = execute_query(
    """
    SELECT
        product_id,
        product_name,
        price
    FROM products
    LIMIT 5;
    """
)

for row in result:
    print(row)