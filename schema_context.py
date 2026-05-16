"""
Session 1 - Step 4
Fetches the AdventureWorks schema and formats it as a string for the LLM prompt.
Command: python schema_context.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# These schemas have no tables — skip them
EXCLUDED_SCHEMAS = {"hr", "pe", "pr", "pu", "sa", "public"}


def get_engine():
    return create_engine(os.getenv("DATABASE_URL"))


def fetch_schema(engine) -> dict:
    """
    Returns a dict like:
    {
      "sales": {
        "salesorderheader": ["salesorderid (integer)", "orderdate (timestamp)", ...],
        "customer": [...],
        ...
      },
      "production": { ... },
      ...
    }
    """
    query = """
        SELECT table_schema, table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
          AND table_schema NOT IN :excluded
        ORDER BY table_schema, table_name, ordinal_position;
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text(query),
            {"excluded": tuple(EXCLUDED_SCHEMAS)}
        ).fetchall()

    schema_dict = {}
    for schema, table, column, dtype in rows:
        schema_dict.setdefault(schema, {}).setdefault(table, []).append(
            f"{column} ({dtype})"
        )
    return schema_dict


def format_schema_for_llm(schema_dict: dict) -> str:
    """
    Converts the schema dict into a plain-text block the LLM can read.

    Example output:
        Schema: sales
        Table: salesorderheader
        Columns: salesorderid (integer), orderdate (timestamp), totaldue (numeric), ...

        Schema: sales
        Table: customer
        Columns: customerid (integer), personid (integer), storeid (integer), ...
    """
    lines = []
    for schema, tables in sorted(schema_dict.items()):
        for table, columns in sorted(tables.items()):
            lines.append(f"Schema: {schema}")
            lines.append(f"Table: {table}")
            lines.append(f"Columns: {', '.join(columns)}")
            lines.append("")  # blank line between tables
    return "\n".join(lines)


def get_schema_context() -> str:
    """Single function the agent will call to get schema context."""
    engine = get_engine()
    schema_dict = fetch_schema(engine)
    return format_schema_for_llm(schema_dict)


if __name__ == "__main__":
    print("Fetching schema from AdventureWorks...\n")
    context = get_schema_context()

    # Count what we have
    engine = get_engine()
    schema_dict = fetch_schema(engine)
    total_tables = sum(len(t) for t in schema_dict.values())
    total_cols = sum(len(c) for t in schema_dict.values() for c in t.values())

    print(f"Schemas : {list(schema_dict.keys())}")
    print(f"Tables  : {total_tables}")
    print(f"Columns : {total_cols}")
    print(f"Context length: {len(context)} characters\n")
    print("--- PREVIEW (first 30 lines) ---")
    print("\n".join(context.splitlines()[:30]))
    print("...(truncated)")
