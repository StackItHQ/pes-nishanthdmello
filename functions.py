def get_sql_rows(sql, table_name):
    try:
        query = f"SELECT * FROM {table_name};"
        sql.execute(query)
        rows = sql.fetchall()
        for i in range(len(rows)):
            rows[i] = list(rows[i])
        return list(rows)
    except:
        return []


def get_sql_headers(sql, table_name):
    try:
        query = f"SELECT * FROM {table_name};"
        sql.execute(query)
        _ = sql.fetchall()
        headers = [i[0] for i in sql.description]
        headers = [i if i != 'NA' else '' for i in headers]
        return headers
    except:
        return[]

def get_google_headers(rows):
    headers = rows.pop(0)
    headers = [i if i != '' else 'NA' for i in headers]
    return headers

def get_google_rows(rows):
    rows = [[i if i != '' else None for i in row] for row in rows]
    return rows