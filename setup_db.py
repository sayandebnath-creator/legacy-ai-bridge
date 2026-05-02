import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("legacy.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS txn_tbl_legacy")

cur.execute("""
CREATE TABLE txn_tbl_legacy (
    txn_id INTEGER,
    amt_val FLOAT,
    dt_rec TEXT,
    usr_cd TEXT
)
""")

users = ["U001", "U002", "USR_X", "A12", None]

base_date = datetime(2024, 1, 1)

for i in range(100):
    amt = round(random.uniform(10, 5000), 2)

    # inconsistent date formats
    dt = base_date + timedelta(days=random.randint(0, 30))
    dt_formats = [
        dt.strftime("%Y-%m-%d"),
        dt.strftime("%d/%m/%Y"),
        dt.strftime("%m-%d-%Y")
    ]

    cur.execute(
        "INSERT INTO txn_tbl_legacy VALUES (?, ?, ?, ?)",
        (i, amt, random.choice(dt_formats), random.choice(users))
    )

conn.commit()
conn.close()

print("Legacy DB created")