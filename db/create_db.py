import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "example.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Drop if exists
c.execute("DROP TABLE IF EXISTS records")

# Create table
c.execute("""
CREATE TABLE records (
    id INTEGER PRIMARY KEY,
    name TEXT,
    details TEXT
)
""")

# Insert demo data
records = [
    (101, "Alice Janssens", "Internal employee – finance department."),
    (202, "Bob Peeters", "Customer ID – active contract."),
    (303, "Carol De Smet", "Supplier record – needs verification."),
    (505, "Delta Team", "Project stakeholder – part of Project Delta initiative.")
]

c.executemany("INSERT INTO records VALUES (?, ?, ?)", records)

conn.commit()
conn.close()

print("Database created at:", DB_PATH)
