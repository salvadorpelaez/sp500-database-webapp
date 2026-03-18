import sqlite3

# Check the actual database at the AI financial company location
db_path = r"c:\Users\salva\OneDrive\Desktop\AI financial company\S&P500_Master.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== CHECKING DATABASE AT AI FINANCIAL COMPANY LOCATION ===")
    print(f"Database path: {db_path}")
    
    # Check table structure
    cursor.execute('PRAGMA table_info(Companies)')
    columns = cursor.fetchall()
    print("\nTable columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Check classification values
    cursor.execute('SELECT Classification, COUNT(*) FROM Companies GROUP BY Classification')
    class_counts = cursor.fetchall()
    print("\nClassification values and counts:")
    for cls, cnt in class_counts:
        if cls is None:
            print(f"  NULL: {cnt}")
        elif cls == '':
            print(f"  EMPTY: {cnt}")
        else:
            print(f"  '{cls}': {cnt}")
    
    # Check for any VALUE classifications
    cursor.execute('SELECT COUNT(*) FROM Companies WHERE Classification = "VALUE"')
    value_count = cursor.fetchone()[0]
    print(f"\nCompanies with Classification = 'VALUE': {value_count}")
    
    # Show some sample data
    cursor.execute('SELECT Ticker, Name, Sector, Classification FROM Companies WHERE Classification IS NOT NULL AND Classification != "" LIMIT 5')
    results = cursor.fetchall()
    print("\nSample companies with classification:")
    for result in results:
        print(f"  {result[0]} - {result[1]} - {result[2]} - Classification: '{result[3]}'")
    
    conn.close()
    
except Exception as e:
    print(f"Error accessing database: {e}")
