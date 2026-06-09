from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

import sqlite3
import pandas as pd
import google.generativeai as genai

# Put your API key here
genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

question = input("Ask a business question: ")

prompt = f"""
You are an expert SQLite SQL generator.

Database schema:

customers(
customer_id,
company_name,
plan
Values: Premium, Basic, Enterprise,
renewal_date
)

product_usage(
customer_id,
product_name
Values: AutoCAD, Fusion, Revit,
hours_used,
last_login
)

support_tickets(
ticket_id,
customer_id,
severity
Values: High, Medium, Low,
status
Values: Open, Closed
)

Rules:
1. Return ONLY SQL.
2. Use exact table names.
3. Use exact column names.
4. Values are case-sensitive.
5. Use SQLite syntax.

Question:
{question}
"""

response = model.generate_content(prompt)

sql_query = response.text.strip()

if "SELECT" in sql_query:
    sql_query = sql_query[sql_query.index("SELECT"):]

sql_query = sql_query.replace("```", "").strip()

if ";" in sql_query:
    sql_query = sql_query[:sql_query.index(";")+1]

# Fix common Gemini capitalization mistakes

sql_query = sql_query.replace("'premium'", "'Premium'")
sql_query = sql_query.replace("'basic'", "'Basic'")
sql_query = sql_query.replace("'enterprise'", "'Enterprise'")

sql_query = sql_query.replace("'open'", "'Open'")
sql_query = sql_query.replace("'closed'", "'Closed'")

sql_query = sql_query.replace("'high'", "'High'")
sql_query = sql_query.replace("'medium'", "'Medium'")
sql_query = sql_query.replace("'low'", "'Low'")

print("\nGenerated SQL:")
print(sql_query)

print("\nRAW RESPONSE:")
print(response.text)

print("\nCLEANED SQL:")
print(sql_query)

conn = sqlite3.connect("company_data.db")

try:
    df = pd.read_sql_query(sql_query, conn)

    print("\nResults:")
    print(df)

except Exception as e:
    print("\nSQL Error:")
    print(e)

    print("\nProblematic SQL:")
    print(sql_query)

conn.close()