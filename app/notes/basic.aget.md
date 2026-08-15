                DATABASE LAYER
                      │
                      ▼
              ┌───────────────┐
              │ SQLAlchemy    │
              │    Engine     │
              └───────┬───────┘
                      │
                      ▼
                PostgreSQL
                      │
                      ▼
              execute_query()
                      │
                      ▼
             Python dictionaries