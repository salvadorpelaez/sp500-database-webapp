import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

# Get all tables
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('Tables in database:')
for table in tables:
    print(f'  Table: {table[0]}')
    
    # Get columns for each table with detailed info
    cursor.execute(f'PRAGMA table_info({table[0]})')
    columns = cursor.fetchall()
    print('  Columns:')
    for col in columns:
        print(f'    {col[1]}')
        # Check if column name contains 'class' (case insensitive)
        if 'class' in col[1].lower():
            print(f'      *** FOUND COLUMN WITH "CLASS": {col[1]} ***')
    
    # Get some sample data to see all columns
    cursor.execute(f'SELECT * FROM {table[0]} LIMIT 3')
    rows = cursor.fetchall()
    if rows:
        print('  Sample data (first 3 rows):')
        for i, row in enumerate(rows):
            print(f'    Row {i+1}: {list(row)}')
    
    print()

conn.close()
