import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

# Add some test classification data for a few companies (using ALL CAPS)
test_data = [
    ('AAPL', 'Apple', 'VALUE'),
    ('MSFT', 'Microsoft', 'BORDERLINE'), 
    ('GOOGL', 'Alphabet', 'HYPERGROWTH'),
    ('AMZN', 'Amazon', 'FLAG')
]

# Clear existing test data first
cursor.execute('UPDATE Companies SET Classification = NULL WHERE Ticker IN (?, ?, ?, ?)', 
               ('AAPL', 'MSFT', 'GOOGL', 'AMZN'))

# Update existing companies with test classifications
for ticker, name, classification in test_data:
    cursor.execute('UPDATE Companies SET Classification = ? WHERE Ticker = ?', (classification, ticker))

# Check the updates
cursor.execute('SELECT Ticker, Name, Classification FROM Companies WHERE Classification IS NOT NULL AND Classification != ""')
results = cursor.fetchall()
print('Updated companies with classifications:')
for result in results:
    print(f'  {result[0]} - {result[1]} - {result[2]}')

conn.commit()
conn.close()
