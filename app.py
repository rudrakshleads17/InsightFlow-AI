import streamlit as st
import google.generativeai as genai
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="InsightFlow AI",
    page_icon="📊",
    layout="wide"
)

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    try:
        api_key = st.secrets["API_KEY"]
    except Exception:
        st.error("API key not found. Please configure .env locally or Streamlit Secrets in deployment.")
        st.stop()

genai.configure(api_key=api_key)

PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-2.0-flash"

primary_model = genai.GenerativeModel(PRIMARY_MODEL)

st.title("📊 InsightFlow AI")
st.subheader("Natural Language Business Intelligence Platform powered by Gemini and SQL Analytics")

st.caption("""
### Example Questions

- Which customers are on Premium plans?
- Show all open support tickets
- Show product usage
- Which products have highest usage?
""")

question = st.text_input(
    "Ask a business question",
    placeholder="Show all open support tickets"
)

if st.button("Generate Insights"):

    if not question.strip():
        st.warning("Please enter a business question.")
        st.stop()

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
1. Return ONLY raw SQL.
2. No markdown.
3. No explanations.
4. Generate only SELECT queries.

Question:
{question}
"""

    try:
        response = primary_model.generate_content(prompt)

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "quota" in error_text.lower():
            st.warning("Gemini 2.5 Flash quota exhausted. Trying Gemini 2.0 Flash...")

            try:
                fallback_model = genai.GenerativeModel(FALLBACK_MODEL)
                response = fallback_model.generate_content(prompt)

            except Exception:
                st.error("Both Gemini 2.5 Flash and Gemini 2.0 Flash are unavailable due to quota limits.")
                st.stop()

        else:
            st.error(f"Gemini Error: {e}")
            st.stop()

    sql_query = response.text.strip()

    if "SELECT" in sql_query:
        sql_query = sql_query[sql_query.index("SELECT"):]

    sql_query = sql_query.replace("```", "").strip()

    if ";" in sql_query:
        sql_query = sql_query[:sql_query.index(";") + 1]

    if not sql_query.upper().startswith("SELECT"):
        st.error("Only SELECT queries are allowed for safety.")
        st.stop()

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    conn = sqlite3.connect("database/company_data.db")

    try:
        df = pd.read_sql_query(sql_query, conn)

        st.subheader("Results")
        st.dataframe(df)

        if len(df.columns) >= 2:
            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) > 0:
                st.subheader("Visualization")
                chart_col = numeric_cols[0]
                st.bar_chart(df[chart_col])

        summary_prompt = f"""
You are a business analyst.

Summarize this business data in 3 bullet points.

Data:
{df.to_string()}
"""

        summary = None

        try:
            summary = primary_model.generate_content(summary_prompt)

        except Exception as e:
            error_text = str(e)

            if "429" in error_text or "quota" in error_text.lower():
                try:
                    insight_model = genai.GenerativeModel(FALLBACK_MODEL)
                    summary = insight_model.generate_content(summary_prompt)

                except Exception:
                    st.warning("Business Insights unavailable due to Gemini API quota limits.")

            else:
                st.error(f"Business Insights Error: {e}")

        if summary:
            st.subheader("Business Insights")
            st.write(summary.text)

    except Exception as e:
        st.error(str(e))

    finally:
        conn.close()