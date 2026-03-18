import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

# Check all classification values
cursor.execute('SELECT Classification, COUNT(*) FROM Companies GROUP BY Classification')
class_counts = cursor.fetchall()
print('All classification values and counts:')
for cls, cnt in class_counts:
    if cls is None:
        print(f'  NULL: {cnt}')
    elif cls == '':
        print(f'  EMPTY: {cnt}')
    else:
        print(f'  "{cls}": {cnt}')

# Check for any VALUE-like values
cursor.execute('SELECT Classification, COUNT(*) FROM Companies WHERE Classification IS NOT NULL AND Classification != "" AND UPPER(Classification) LIKE "%VALUE%" GROUP BY Classification')
value_like = cursor.fetchall()
print('\nVALUE-like classifications:')
for cls, cnt in value_like:
    print(f'  "{cls}": {cnt}')

conn.close()
