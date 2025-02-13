def validate_sql(sql_query):
    prohibited_keywords = ["DROP", "DELETE", "UPDATE", "ALTER"]
    for keyword in prohibited_keywords:
        if keyword in sql_query.upper():
            return False
    return True