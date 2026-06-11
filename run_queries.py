import sqlite3
import pandas as pd

DB_PATH = "hospital.db"
SQL_FILE = "sql/queries.sql"

SKIP_KEYWORDS = ("create table", "copy ")

def load_queries(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    raw_statements = content.split(";")
    queries = []
    for stmt in raw_statements:
        lines = [l for l in stmt.splitlines() if not l.strip().startswith("--")]
        clean = "\n".join(lines).strip()
        if not clean:
            continue
        if any(clean.lower().startswith(kw) for kw in SKIP_KEYWORDS):
            print(f"  [SKIPPED] {clean[:60].strip()} ...")
            continue
        queries.append(clean)
    return queries

conn = sqlite3.connect(DB_PATH)

print(f"\nRunning: {SQL_FILE}")
print("=" * 60)

queries = load_queries(SQL_FILE)

for i, query in enumerate(queries, 1):
    label = next((l.strip().lstrip("--").strip()
                  for l in query.splitlines() if l.strip()), query[:60])
    print(f"\nQuery {i}: {label[:80]}")
    print("-" * 60)
    try:
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
    except Exception as e:
        print(f"  ERROR: {e}")

conn.close()
print("\n" + "=" * 60)
print("All queries done.")
