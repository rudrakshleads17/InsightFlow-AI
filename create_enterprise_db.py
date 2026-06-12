import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("database/company_data.db")
cursor = conn.cursor()

# Remove old tables

cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("DROP TABLE IF EXISTS support_tickets")
cursor.execute("DROP TABLE IF EXISTS revenue")

# Customers

cursor.execute("""
CREATE TABLE customers(
    customer_id INTEGER PRIMARY KEY,
    company_name TEXT,
    plan TEXT,
    renewal_date TEXT
)
""")

# Employees

cursor.execute("""
CREATE TABLE employees(
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT,
    department TEXT,
    salary INTEGER
)
""")

# Sales

cursor.execute("""
CREATE TABLE sales(
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_name TEXT,
    amount INTEGER,
    sale_date TEXT
)
""")

# Support Tickets

cursor.execute("""
CREATE TABLE support_tickets(
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    severity TEXT,
    status TEXT
)
""")

# Revenue

cursor.execute("""
CREATE TABLE revenue(
    month TEXT,
    revenue INTEGER
)
""")

plans = ["Basic", "Premium", "Enterprise"]

products = [
    "AutoCAD",
    "Fusion",
    "Revit",
    "Inventor",
    "Civil 3D"
]

departments = [
    "Sales",
    "Engineering",
    "HR",
    "Finance",
    "Support"
]

# Customers

for i in range(1, 101):

    company = f"Company_{i}"

    plan = random.choice(plans)

    renewal = (
        datetime.now() +
        timedelta(days=random.randint(30, 365))
    ).strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO customers VALUES (?,?,?,?)",
        (i, company, plan, renewal)
    )

# Employees

for i in range(1, 101):

    cursor.execute(
        "INSERT INTO employees VALUES (?,?,?,?)",
        (
            i,
            f"Employee_{i}",
            random.choice(departments),
            random.randint(30000, 150000)
        )
    )

# Sales

for i in range(1, 501):

    cursor.execute(
        "INSERT INTO sales VALUES (?,?,?,?,?)",
        (
            i,
            random.randint(1, 100),
            random.choice(products),
            random.randint(500, 10000),
            (
                datetime.now() -
                timedelta(days=random.randint(1, 365))
            ).strftime("%Y-%m-%d")
        )
    )

# Tickets

for i in range(1, 201):

    cursor.execute(
        "INSERT INTO support_tickets VALUES (?,?,?,?)",
        (
            i,
            random.randint(1, 100),
            random.choice(
                ["High", "Medium", "Low"]
            ),
            random.choice(
                ["Open", "Closed"]
            )
        )
    )

# Revenue

months = [
    "Jan","Feb","Mar","Apr",
    "May","Jun","Jul","Aug",
    "Sep","Oct","Nov","Dec"
]

for m in months:

    cursor.execute(
        "INSERT INTO revenue VALUES (?,?)",
        (
            m,
            random.randint(
                100000,
                1000000
            )
        )
    )

conn.commit()
conn.close()

print("Enterprise Database Created Successfully")