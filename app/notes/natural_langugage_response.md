You: Who has spent the most money?

========== CLASSIFICATION ==========
ambiguous

========== REASONING ==========
The question is ambiguous because there are multiple possible interpretations of who has spent the most money, such as total revenue or average order value.

Agent:
Do you want to know which customer has spent the most money in total, or are you looking for the customer with the highest average order value?

You: customer with the highest average order value

========== COMBINED QUESTION ==========

Original user question:
Who has spent the most money?

Clarification question:
Do you want to know which customer has spent the most money in total, or are you looking for the customer with the highest average order value?

User's clarification:
customer with the highest average order value


========== GENERATED SQL ==========
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, AVG(o.total_amount) AS average_order_value FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY average_order_value DESC LIMIT 1

========== VALIDATED SQL ==========
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, AVG(o.total_amount) AS average_order_value FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY average_order_value DESC LIMIT 1

Agent:
The customer with the highest average order value is Patricia Ellison, with an average order value of $7,944.22.

