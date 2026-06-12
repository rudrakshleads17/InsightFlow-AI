

import streamlit as st
import google.generativeai as genai

api_key = st.secrets["API_KEY"]

st.write("API key loaded:", api_key is not None)
st.write("API key length:", len(api_key) if api_key else 0)


genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

st.write("App started")
st.write("Secret exists")

#Tempppppppppppppppppppppppppppppppppppppppppppppppp

st.set_page_config(
    page_title="InsightFlow AI",
    page_icon="📊",
    layout="wide"
)

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

# ---------------------------
# BUTTON
# ---------------------------

if st.button("Generate Insights"):

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

Question:
{question}
"""

    try:
    response = model.generate_content(prompt)

except Exception as e:
    st.error(f"Gemini Error: {e}")
    st.stop()

sql_query = response.text.strip()

    if "SELECT" in sql_query:
        sql_query = sql_query[sql_query.index("SELECT"):]

    sql_query = sql_query.replace("```", "").strip()

    if ";" in sql_query:
        sql_query = sql_query[:sql_query.index(";")+1]

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    conn = sqlite3.connect("company_data.db")

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

        # AI Business Summary

        summary_prompt = f"""
        Summarize this business data in 3 bullet points.

        Data:
        {df.to_string()}
        """

        summary = model.generate_content(summary_prompt)

        st.subheader("Business Insights")

        st.write(summary.text)

    except Exception as e:

        st.error(str(e))

    conn.close()
