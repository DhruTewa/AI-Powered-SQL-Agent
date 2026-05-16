def validate_sql(sql: str) -> str:
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER"]
    sql_upper = sql.upper()
    for word in forbidden:
        if word in sql_upper:
            raise ValueError(f"Forbidden keyword found in the query: {word}")
    return sql