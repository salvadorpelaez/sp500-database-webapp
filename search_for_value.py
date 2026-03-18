import sqlite3
import os

db_path = r"c:\Users\salva\OneDrive\Desktop\AI financial company\S&P500_Master.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== CHECKING FOR CLASSIFICATION DATA IN OTHER COLUMNS ===")

# Check all columns for any VALUE-like data
cursor.execute('PRAGMA table_info(Companies)')
columns = cursor.fetchall()

for col in columns:
    col_name = col[1]
    if col_name.lower() in ['classification', 'class', 'category', 'type', 'grade']:
        cursor.execute(f'SELECT DISTINCT {col_name} FROM Companies WHERE {col_name} IS NOT NULL AND {col_name} != "" LIMIT 10')
        values = cursor.fetchall()
        if values:
            print(f"\n{col_name} values:")
            for val in values:
                print(f"  '{val[0]}'")

# Check for VALUE in any text column
print("\n=== SEARCHING FOR 'VALUE' IN ALL TEXT COLUMNS ===")
text_columns = [col[1] for col in columns if col[2] in ['TEXT', 'VARCHAR']]

for col_name in text_columns:
    cursor.execute(f'SELECT COUNT(*) FROM Companies WHERE UPPER({col_name}) LIKE "%VALUE%"')
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"{col_name}: {count} rows contain 'VALUE'")
        cursor.execute(f'SELECT Ticker, Name, {col_name} FROM Companies WHERE UPPER({col_name}) LIKE "%VALUE%" LIMIT 3')
        results = cursor.fetchall()
        for result in results:
            print(f"  {result[0]} - {result[1]} - {col_name}: '{result[2]}'")

# Check if there are other tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nTables in database: {[t[0] for t in tables]}")

conn.close()
