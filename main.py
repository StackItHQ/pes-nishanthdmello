import sys
import argparse
import gspread
from google.oauth2.service_account import Credentials
from MySQL_Connection import connect_to_mysql
from functions import *
import time


conn=connect_to_mysql()
sql = conn.cursor()


parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True, help="google sheet url")
parser.add_argument("--cred", required=True, help="credentials json file")
args = parser.parse_args()
url = args.url
cred = args.cred
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(cred, scopes=scope)
client = gspread.authorize(creds)


try:
    sheet = client.open_by_url(url)
except:
    print("Run python3 main.py --url <google sheet url>")
    sys.exit()


try:
    database = sheet.title
    query = f"CREATE DATABASE IF NOT EXISTS {database};"
    sql.execute(query)
    query = f"USE {database};"
    sql.execute(query)
    conn.commit()
except:
    print('creation of database failed...')


try:
    table = sheet.get_worksheet(0)
    table_name = table.title
except:
    print('getting table from google sheets failed...')


# google sheet to sql
try:
    data = table.get_all_values()
    headers = get_google_headers(data)
    rows = get_google_rows(data)
    print(headers)
    print(rows)
    query = f"DROP TABLE IF EXISTS {table_name};"
    sql.execute(query)
    conn.commit()
    if headers or rows:
        query = f"CREATE TABLE {table_name} (" + ", ".join([f"`{header}` VARCHAR(255)" for header in headers if header]) + ");"
        sql.execute(query)
        query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['%s'] * len(headers))});"
        for row in rows:
            sql.execute(query, row)
        conn.commit()
except:
    print('failed to put data from google sheets to sql...')


# sql to google sheet
try:
    rows = get_sql_rows(sql, table_name)
    headers = get_sql_headers(sql, table_name)
    data = [headers] + rows
    print(data)

    table.clear()
    table.update(values=data, range_name='A1')
except:
    print('failed to put data from sql to google sheets...')
