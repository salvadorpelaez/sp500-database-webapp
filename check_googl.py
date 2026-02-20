import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

cursor.execute('SELECT Name FROM Companies WHERE Ticker = ?', ('GOOGL',))
result = cursor.fetchone()

if result:
    print(f'GOOGL Name in database: {result[0]}')
else:
    print('GOOGL not found in database')

conn.close()
