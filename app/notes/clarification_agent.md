architecture
                  User
                   │
                   ▼
          Clarification Agent
                   │
        ┌──────────┼───────────┐
        ▼          ▼           ▼
      CLEAR    AMBIGUOUS    INCOMPLETE
        │          │           │
        ▼          ▼           ▼
    SQL Agent   Ask user    Ask user
        │
        ▼
     SQLGlot
        │
        ▼
   PostgreSQL


## testing clarrfication agent with asking multiple question

output:

================================
QUESTION:
How many orders were placed last month?

CLASSIFICATION:
clear

REASONING:
The question is clear and provides enough information to determine exactly what data should be queried, which is the number of orders placed last month.

CLARIFICATION:


================================
QUESTION:
Who is the best customer?

CLASSIFICATION:
ambiguous

REASONING:
The question 'Who is the best customer?' is ambiguous because there are multiple possible interpretations of what 'best customer' means, such as highest total revenue, most orders, or highest average order value.

CLARIFICATION:
What do you mean by 'best customer'? Do you want to know the customer with the highest total revenue, the most orders, or the highest average order value?

================================
QUESTION:
Show me sales for

CLASSIFICATION:
incomplete

REASONING:
The question is incomplete because it does not specify what type of sales or the time period for which sales are being requested.

CLARIFICATION:
What type of sales are you looking for (e.g. by customer, product, category, date range)?

================================
QUESTION:
What is the weather today?

CLASSIFICATION:
invalid

REASONING:
The question is unrelated to the available database and cannot reasonably be answered using the provided schema. 

### QUESTION:
Who is the best customer?

CLASSIFICATION:
ambiguous

REASONING:
The question 'Who is the best customer?' is ambiguous because there are multiple possible interpretations of what 'best customer' means, such as highest total revenue, most orders, or highest average order value.

CLARIFICATION:
What do you mean by 'best customer'? Do you want to know the customer with the highest total revenue, the most orders, or the highest average order value?