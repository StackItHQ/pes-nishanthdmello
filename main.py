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
