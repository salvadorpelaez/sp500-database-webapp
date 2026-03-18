import sqlite3

def check_database():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    # Check all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables in database: {tables}")
    
    # Check if NASDAQ table exists
    if 'NASDAQ' in tables:
        cursor.execute("PRAGMA table_info(NASDAQ);")
        columns = cursor.fetchall()
        print(f"\nNASDAQ table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Check row count
        cursor.execute("SELECT COUNT(*) FROM NASDAQ;")
        count = cursor.fetchone()[0]
        print(f"\nNASDAQ table has {count} rows")
    else:
        print("\nNASDAQ table does not exist")
    
    conn.close()

if __name__ == "__main__":
    check_database()
