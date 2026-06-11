import pandas as pd
import sqlite3
import os

CSV_PATH = "data/hospital_cleaned.csv"
DB_PATH = "hospital.db"
TABLE_NAME = "hospital_patients"

# Remove old DB so we always start fresh
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"Removed existing {DB_PATH}")

# Load CSV
print(f"Reading {CSV_PATH} ...")
df = pd.read_csv(CSV_PATH)
print(f"CSV loaded — {len(df)} rows, {len(df.columns)} columns")

# Write to SQLite
conn = sqlite3.connect(DB_PATH)
df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
conn.commit()

# Verify row count
cursor = conn.cursor()
cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
row_count = cursor.fetchone()[0]
print(f"Rows loaded into '{TABLE_NAME}': {row_count}")

# Verify table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables in {DB_PATH}: {tables}")

conn.close()
print("Done.")
