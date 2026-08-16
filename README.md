# Text-to-SQL with a Clarification Engine


> A production-oriented Text-to-SQL system that converts natural-language questions into PostgreSQL queries and, in later phases, intelligently asks for clarification when a user's question is ambiguous.
<img width="1257" height="817" alt="image" src="https://github.com/user-attachments/assets/1f23ff65-a757-49b6-8414-7cca151ee878" />

---

## 🚧 Project Status

**Current Status: Phase 3 — Basic Text-to-SQL completed**

The current system can:

- Convert natural-language questions into SQL
- Use PostgreSQL as the database
- Use Groq as the default LLM
- Automatically fall back to Gemini if Groq fails
- Execute generated SQL against PostgreSQL
- Return database results to the user
- Work with multiple tables and SQL JOINs

The **Clarification Engine is not implemented yet**. It is the core feature planned for the next phases.

---

# 🎯 Project Goal

Traditional Text-to-SQL systems focus mainly on:

```text
Natural Language
       ↓
      LLM
       ↓
      SQL
       ↓
   Database
       ↓
    Result
```
This works well when the user's question is clear.

However, real users often ask ambiguous questions.

For example:

"Who is the best customer?"

What does best mean?

It could mean:

Customer with the highest revenue
Customer with the most orders
Customer with the highest average order value
Customer with the most recent purchases

A basic Text-to-SQL system may simply choose one interpretation and generate SQL.

That can produce a technically valid query but the wrong answer.

### This project aims to solve that problem by introducing a Clarification Engine between the user and the Text-to-SQL system.

## core idea!
```
User Question
      ↓
Clarification Engine
      ↓
Is the question ambiguous?
      │
      ├─────────────── NO ──────────────┐
      │                                 ↓
     YES                          Text-to-SQL Engine
      ↓                                 ↓
Ask clarification                  SQL Validation
      ↓                                 ↓
User provides context              PostgreSQL
      ↓                                 ↓
      └───────────────→              Result
                                        ↓
                                  Natural Language
                                     Response
```
# 🏗️ Final Architecture
```
                         ┌───────────────────┐
                         │       User        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                     ┌─────────────────────────┐
                     │  Clarification Engine   │
                     │                         │
                     │ Is the user's intent    │
                     │ clear or ambiguous?     │
                     └────────────┬────────────┘
                                  │
                       ┌──────────┴──────────┐
                       │                     │
                    Ambiguous              Clear
                       │                     │
                       ▼                     ▼
              Ask clarification       Text-to-SQL
                       │                     │
                       │                     ▼
                       │              SQL Validation
                       │                     │
                       │                     ▼
                       │                PostgreSQL
                       │                     │
                       │                     ▼
                       └──────────────►  Result
                                             │
                                             ▼
                                      Final Response
```
#📁 Current Project Structure
```
text-to-sql-clarification-engine/
│
├── app/
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── providers.py
│   │   └── manager.py
│   │
│   ├── text_to_sql/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── prompts.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   │
│   └── main.py
│
├── database/
│   ├── schema.sql
│   └── seed.py
│
├── tests/
│
├── docs/
│
├── .env
├── .gitignore
└── requirements.txt
```
### A Real Problem We Discovered
A Real Problem We Discovered
```Which customer has spent the most money?```
The LLM initially generated:
```
SELECT c.nameFROM customers c....
```
PostgreSQL returned:
```column c.name does not exist```
Why?
Because the actual database contains:
first_name
last_name

instead of name,
This exposed an important Text-to-SQL problem:
### The LLM's understanding of the database schema must match the actual database schema.

We fixed this by providing the actual database schema to the model.
The prompt now explicitly tells the model:

## end-to-end Text-to-SQL pipeline:
```
                    USER
                     │
                     │
       "How many orders last month?"
                     │
                     ▼
              ┌─────────────┐
              │   Generator │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Groq /      │
              │ Gemini      │
              └──────┬──────┘
                     │
                     ▼
              SQLGenerationResult
                │      │      │
                │      │      └── tables_used
                │      └───────── explanation
                └──────────────── sql
                     │
                     ▼
              execute_query()
                     │
                     ▼
                PostgreSQL
                     │
                     ▼
                  Result
```

clarification agent is actually working correctly
currently this is how it works:
```
User Question
      ↓
Clarification Agent
      ↓
┌──────────┬────────────┬────────────┬─────────┐
│  Clear   │ Ambiguous  │ Incomplete │ Invalid │
└────┬─────┴─────┬──────┴──────┬─────┴────┬────┘
     │           │             │           │
     ↓           ↓             ↓           ↓
Generate SQL   Ask user      Ask user    Reject
```
next step is too implement the conversation loop where we combined the original question with clarification question 
like this 
```
Original:
Who is the best customer?

Clarification:
Highest total revenue.
```
This is now a proper Clarification → Text-to-SQL → Validation → Execution pipeline.

<img width="1627" height="486" alt="image" src="https://github.com/user-attachments/assets/87901ccf-7fc7-48eb-8dc2-2d046b586ff4" />


<img width="1506" height="933" alt="image" src="https://github.com/user-attachments/assets/628b8265-8ea4-456b-8fda-249d2643f1fa" />


## Natural-language response generation is now fully integrated
```
User question
      ↓
Clarification
      ↓
User answer
      ↓
SQL generation
      ↓
Validation
      ↓
Database
      ↓
Natural-language response
```
```
Direct question
→ SQL → Validate → Execute → Natural Answer
```
and
```
Ambiguous question
→ Clarification → SQL → Validate → Execute → Natural Answer
```
So this feature is complete. 🎯

Already completed
```
✅ PostgreSQL database
✅ E-commerce schema
✅ Realistic seed data
✅ .env configuration
✅ Groq integration
✅ Gemini integration/fallback
✅ LLM manager
✅ SQL generation
✅ Pydantic structured output
✅ Clarification classification
✅ Clear question handling
✅ Ambiguous question handling
✅ Incomplete question handling
✅ Invalid question handling
✅ Two-turn clarification
✅ SQLGlot validation
✅ PostgreSQL execution
✅ Basic orchestration
✅ Interactive main.py
✅ Natural language response
✅ handles database empty result
```

### still working on......
