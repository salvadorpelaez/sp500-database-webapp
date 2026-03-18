import sqlite3

# Check the database in the app directory
conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

# Check table structure
cursor.execute('PRAGMA table_info(Companies)')
columns = cursor.fetchall()
print('Columns in Companies table:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

# Check if there's data
cursor.execute('SELECT COUNT(*) FROM Companies')
count = cursor.fetchone()[0]
print(f'\nTotal companies: {count}')

# Get sample data
cursor.execute('SELECT * FROM Companies LIMIT 3')
results = cursor.fetchall()
print('\nSample data:')
for result in results:
    print(f'  {result}')

conn.close()
