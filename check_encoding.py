import sqlite3

def check_googl_encoding():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    # Get raw bytes and decoded text
    cursor.execute('SELECT Name FROM Companies WHERE Ticker = ?', ('GOOGL',))
    result = cursor.fetchone()
    
    if result:
        raw_name = result[0]
        print(f"Raw data type: {type(raw_name)}")
        print(f"Raw data: {repr(raw_name)}")
        print(f"Display: {raw_name}")
        
        # Check for problematic characters
        for i, char in enumerate(raw_name):
            if ord(char) > 127:  # Non-ASCII character
                print(f"Position {i}: '{char}' (Unicode: {ord(char)})")
    
    conn.close()

def check_all_problematic_names():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT Ticker, Name FROM Companies WHERE Name LIKE "%?%" OR Name LIKE "%�%"')
    results = cursor.fetchall()
    
    print(f"Found {len(results)} names with potential encoding issues:")
    for ticker, name in results:
        print(f"  {ticker}: {repr(name)}")
    
    conn.close()

if __name__ == "__main__":
    print("=== GOOGL Encoding Analysis ===")
    check_googl_encoding()
    
    print("\n=== All Problematic Names ===")
    check_all_problematic_names()
