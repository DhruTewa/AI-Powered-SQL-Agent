"""
Session 1 - Step 3
Run this to verify your AdventureWorks connection and explore its schema.
Command: python explore_db.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    engine = create_engine(DATABASE_URL)
    return engine


def list_schemas(engine):
    query = """
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
        ORDER BY schema_name;
    """
    with engine.connect() as conn:
        rows = conn.execute(text(query)).fetchall()
    return [r[0] for r in rows]


def list_tables_in_schema(engine, schema):
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = :schema
          AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """
    with engine.connect() as conn:
        rows = conn.execute(text(query), {"schema": schema}).fetchall()
    return [r[0] for r in rows]


def get_columns(engine, schema, table):
    query = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = :schema
          AND table_name = :table
        ORDER BY ordinal_position;
    """
    with engine.connect() as conn:
        rows = conn.execute(text(query), {"schema": schema, "table": table}).fetchall()
    return rows


if __name__ == "__main__":
    print("Connecting to AdventureWorks...\n")
    engine = get_connection()

    schemas = list_schemas(engine)
    print(f"Found {len(schemas)} schemas: {schemas}\n")

    for schema in schemas:
        tables = list_tables_in_schema(engine, schema)
        print(f"  [{schema}] — {len(tables)} tables")
        for table in tables:
            cols = get_columns(engine, schema, table)
            col_summary = ", ".join(f"{c[0]} ({c[1]})" for c in cols[:4])
            print(f"    {schema}.{table}: {col_summary} ...")

    print("\nConnection successful.")
