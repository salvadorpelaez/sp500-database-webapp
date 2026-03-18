import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

# Execute the exact query
cursor.execute("SELECT * FROM Companies WHERE Sector = 'Energy' AND Classification = 'VALUE'")
results = cursor.fetchall()

print(f"Found {len(results)} companies with Sector='Energy' and Classification='VALUE':")
for result in results:
    print(f"  {result[1]} - {result[2]} - Sector: {result[3]} - Classification: {result[9]}")

conn.close()
