import sqlite3
import os

db_path = r"c:\Users\salva\OneDrive\Desktop\AI financial company\S&P500_Master.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== CHECKING STAGING_UPDATES TABLE ===")
try:
    cursor.execute('PRAGMA table_info(Staging_Updates)')
    columns = cursor.fetchall()
    print("Staging_Updates columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    cursor.execute('SELECT COUNT(*) FROM Staging_Updates')
    count = cursor.fetchone()[0]
    print(f"\nRows in Staging_Updates: {count}")
    
    if count > 0:
        cursor.execute('SELECT * FROM Staging_Updates LIMIT 3')
        results = cursor.fetchall()
        print("\nSample data from Staging_Updates:")
        for result in results:
            print(f"  {result}")
            
except Exception as e:
    print(f"Error with Staging_Updates: {e}")

print("\n=== CHECKING FOR OTHER DATABASE FILES ===")
db_dir = r"c:\Users\salva\OneDrive\Desktop\AI financial company"
db_files = [f for f in os.listdir(db_dir) if f.endswith('.db')]
print(f"Database files found: {db_files}")

# Check if there's a different database with classification data
for db_file in db_files:
    if db_file != 'S&P500_Master.db':
        full_path = os.path.join(db_dir, db_file)
        try:
            conn2 = sqlite3.connect(full_path)
            cursor2 = conn2.cursor()
            cursor2.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor2.fetchall()
            print(f"\n{db_file} tables: {[t[0] for t in tables]}")
            conn2.close()
        except Exception as e:
            print(f"Error checking {db_file}: {e}")

conn.close()
