# Text-to-SQL Clarification Agent — Question Dataset

## Purpose

This document contains the initial evaluation question set for the E-commerce Text-to-SQL Clarification Agent.

The questions are divided into four categories:

- **Clear** — The user's intent is specific enough to generate SQL directly.
- **Ambiguous** — Multiple reasonable interpretations exist, so the agent should ask for clarification.
- **Incomplete** — Important information is missing, so the agent should ask for clarification.
- **Invalid** — The question is outside the scope of the available e-commerce database or requests an unsupported operation.

The dataset contains **40 questions** in total.

---

# 1. Clear Questions

These questions should be answerable directly from the database without asking the user for clarification.

| # | Question | Classification |
|---|---|---|
| 1 | How many orders were placed last month? | Clear |
| 2 | What is our average order value? | Clear |
| 3 | What is the total revenue from all orders? | Clear |
| 4 | How many orders were placed this year? | Clear |
| 5 | Which product sells the most units? | Clear |
| 6 | Which product generated the most revenue? | Clear |
| 7 | What are the top 10 products by revenue? | Clear |
| 8 | Which category generated the most revenue? | Clear |
| 9 | How many customers have placed at least one order? | Clear |
| 10 | Which customer has spent the most money? | Clear |
| 11 | Which customer has placed the most orders? | Clear |
| 12 | How many customers have never placed an order? | Clear |
| 13 | What was the total revenue last month? | Clear |
| 14 | How many orders were cancelled last month? | Clear |
| 15 | How many successful payments were made this month? | Clear |
| 16 | Which payment method is used most often? | Clear |
| 17 | Which products have less than 10 units in stock? | Clear |
| 18 | What is the average product price? | Clear |
| 19 | Which country has the most customers? | Clear |
| 20 | How many new customers signed up this year? | Clear |

---

# 2. Ambiguous Questions

These questions have enough information to understand the general topic, but the intended metric or meaning is unclear.

The agent should **not guess**. It should ask a clarification question.

| # | Question | Classification | Possible Interpretations |
|---|---|---|---|
| 21 | Who is the best customer? | Ambiguous | Highest spending, most orders, highest average order value |
| 22 | Which product is the best? | Ambiguous | Highest revenue, highest quantity sold, highest profit |
| 23 | What are our top products? | Ambiguous | Top by revenue, quantity sold, or profit |
| 24 | Which customers are most valuable? | Ambiguous | Highest spending, most orders, highest profit |
| 25 | Which products are performing well? | Ambiguous | Revenue, quantity sold, profit, or growth |
| 26 | What are our best categories? | Ambiguous | Revenue, quantity sold, or profit |
| 27 | Which customers are most active? | Ambiguous | Most orders, highest spending, or most recent purchases |
| 28 | What is our strongest market? | Ambiguous | Revenue, order count, or customer count |
| 29 | Which month was the best? | Ambiguous | Highest revenue, most orders, or highest profit |
| 30 | Which products should we focus on? | Ambiguous | Highest sales, highest profit, high demand, or low inventory |

### Example clarification

User:

```text
Who is the best customer?
```

Agent should respond with something like:

```text
What should "best customer" mean: highest total spending,
most orders, or highest average order value?
```

The agent should generate SQL only after the ambiguity is resolved.

---

# 3. Incomplete Questions

These questions do not provide enough information to construct the intended query.

The agent should ask for the missing information.

| # | Question | Classification | Missing Information |
|---|---|---|---|
| 31 | Show me the sales. | Incomplete | Time period and/or grouping |
| 32 | Show me the revenue. | Incomplete | Time period |
| 33 | Show me the orders. | Incomplete | Which orders or time period |
| 34 | Show me the customers. | Incomplete | What customer information is needed |
| 35 | Show me recent orders. | Incomplete | Definition of "recent" |
| 36 | Give me the top customers. | Incomplete | Metric for ranking customers |
| 37 | Compare our sales. | Incomplete | What should be compared |
| 38 | Show me product performance. | Incomplete | Performance metric and/or time period |

### Example clarification

User:

```text
Show me the sales.
```

Agent should ask:

```text
What time period would you like to see?
```

If the user answers:

```text
This year.
```

The agent can continue only if another required detail is still missing.

---

# 4. Invalid Questions

These questions are outside the capabilities of the initial e-commerce database or request unsupported database operations.

The agent should **not generate SQL** for these requests.

| # | Question | Classification | Reason |
|---|---|---|---|
| 39 | What is the weather in Mumbai? | Invalid | Weather data is not available |
| 40 | What is today's cricket score? | Invalid | Sports data is not available |
| 41 | What is the current stock price of Apple? | Invalid | Stock market data is not available |
| 42 | What is the population of India? | Invalid | Population data is not available |
| 43 | Send an email to our top customer. | Invalid | Email actions are outside the initial read-only scope |
| 44 | Delete all cancelled orders. | Invalid | Database modification is not allowed |
| 45 | Update the price of all products by 10%. | Invalid | Database modification is not allowed |
| 46 | Drop the payments table. | Invalid | Destructive database operation is not allowed |

---

# 5. Expected Agent Behavior

## Clear

```text
User Question
     ↓
Classify as Clear
     ↓
Generate SQL
     ↓
Validate SQL
     ↓
Execute SQL
     ↓
Return Business Answer
```

Example:

```text
User:
How many orders were placed last month?

Agent:
There were 1,247 orders placed last month.
```

---

## Ambiguous

```text
User Question
     ↓
Classify as Ambiguous
     ↓
Identify possible meanings
     ↓
Ask clarification
     ↓
User provides intent
     ↓
Generate SQL
```

Example:

```text
User:
Who is the best customer?

Agent:
Do you mean the customer with the highest total spending,
the most orders, or the highest average order value?
```

---

## Incomplete

```text
User Question
     ↓
Classify as Incomplete
     ↓
Identify missing information
     ↓
Ask clarification
     ↓
User provides missing information
     ↓
Generate SQL
```

Example:

```text
User:
Show me the revenue.

Agent:
What time period should I use?
```

---

## Invalid

```text
User Question
     ↓
Classify as Invalid
     ↓
Do not generate SQL
     ↓
Explain limitation
```

Example:

```text
User:
What is the weather in Mumbai?

Agent:
I can answer questions about the e-commerce database,
but weather information is not available in the current dataset.
```

---

# 6. Dataset Summary

| Classification | Number of Questions |
|---|---:|
| Clear | 20 |
| Ambiguous | 10 |
| Incomplete | 8 |
| Invalid | 8 |
| **Total** | **46** |

> Note: The dataset intentionally contains more than 40 questions so that there are enough examples in each category for testing the clarification agent.

---

# 7. Core Principle

The most important behavior of this project is:

> **The agent should clarify uncertainty instead of guessing user intent.**

A traditional Text-to-SQL system may immediately generate SQL for a question such as:

```text
Who is the best customer?
```

This project should instead recognize that "best" is undefined and ask the user what metric they mean.

This clarification-first approach is the core feature that differentiates this project from a basic Text-to-SQL system.
