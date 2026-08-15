import sqlglot
from sqlglot import exp


class SQLValidationError(Exception):
    """Raised when generated SQL fails validation."""


def validate_sql(sql: str) -> str:
    """
    Validate generated SQL before it reaches PostgreSQL.

    Rules:
    - SQL must be valid PostgreSQL syntax.
    - Only SELECT statements are allowed.
    - Multiple statements are rejected.
    - Write/destructive operations are rejected.
    """

    if not sql or not sql.strip():
        raise SQLValidationError("SQL query is empty.")

    sql = sql.strip()

    # Parse using PostgreSQL dialect
    try:
        statements = sqlglot.parse(
            sql,
            dialect="postgres",
        )
    except sqlglot.errors.ParseError as exc:
        raise SQLValidationError(
            f"Invalid SQL syntax: {exc}"
        ) from exc

    # Don't allow multiple SQL statements
    if len(statements) != 1:
        raise SQLValidationError(
            "Multiple SQL statements are not allowed."
        )

    statement = statements[0]

    # Only SELECT queries are allowed
    if not isinstance(statement, exp.Select):
        raise SQLValidationError(
            "Only SELECT queries are allowed."
        )

    return sql