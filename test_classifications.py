import sqlite3

db_path = r'c:\Users\salva\OneDrive\Desktop\AI financial company\S&P500_Master.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check the exact data in Classification column
cursor.execute("SELECT Classification, COUNT(*) FROM Companies GROUP BY Classification ORDER BY COUNT(*) DESC")
results = cursor.fetchall()

print('Classification column data:')
for result in results:
    classification = result[0] if result[0] else 'NULL/Empty'
    count = result[1]
    print(f'  "{classification}": {count} companies')

# Check a few sample rows with Classification
cursor.execute("SELECT Name, Classification FROM Companies WHERE Classification IS NOT NULL LIMIT 10")
samples = cursor.fetchall()
print('\nSample rows with Classification:')
for sample in samples:
    print(f'  {sample[0]}: "{sample[1]}"')

conn.close()
