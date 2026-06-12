import sqlite3

conn = sqlite3.connect("company_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE customers(
customer_id INTEGER,
company_name TEXT,
plan TEXT,
renewal_date TEXT
)
""")

cursor.execute("""
CREATE TABLE product_usage(
customer_id INTEGER,
product_name TEXT,
hours_used INTEGER,
last_login TEXT
)
""")

cursor.execute("""
CREATE TABLE support_tickets(
ticket_id INTEGER,
customer_id INTEGER,
severity TEXT,
status TEXT
)
""")

customers = [
(1,"ABC Engineering","Premium","2026-07-15"),
(2,"BuildTech","Basic","2026-06-25"),
(3,"Skyline Infra","Premium","2026-08-01"),
(4,"NextGen Design","Enterprise","2026-06-20"),
(5,"Urban Structures","Basic","2026-07-10")
]

usage = [
(1,"AutoCAD",240,"2026-06-08"),
(2,"Fusion",120,"2026-06-07"),
(3,"Revit",300,"2026-06-08"),
(4,"AutoCAD",500,"2026-06-09"),
(5,"Fusion",80,"2026-06-05")
]

tickets = [
(101,1,"High","Open"),
(102,2,"Low","Closed"),
(103,3,"Medium","Open"),
(104,4,"High","Closed"),
(105,5,"Low","Open")
]

cursor.executemany(
"INSERT INTO customers VALUES (?,?,?,?)",
customers
)

cursor.executemany(
"INSERT INTO product_usage VALUES (?,?,?,?)",
usage
)

cursor.executemany(
"INSERT INTO support_tickets VALUES (?,?,?,?)",
tickets
)

conn.commit()
conn.close()

print("Database Created Successfully")