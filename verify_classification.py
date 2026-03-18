import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

# Check if classification data exists
cursor.execute('SELECT Ticker, Name, Classification FROM Companies WHERE Classification IS NOT NULL AND Classification != "" LIMIT 5')
results = cursor.fetchall()
print('Companies with classification data:')
for result in results:
    print(f'  {result[0]} - {result[1]} - Classification: "{result[2]}"')

# Check total count
cursor.execute('SELECT COUNT(*) FROM Companies WHERE Classification IS NOT NULL AND Classification != ""')
count = cursor.fetchone()[0]
print(f'\nTotal companies with classification: {count}')

conn.close()
