import sqlite3

def analyze_character_encoding():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    # Check GOOG (which still has the issue)
    cursor.execute('SELECT Name FROM Companies WHERE Ticker = ?', ('GOOG',))
    goog_result = cursor.fetchone()
    
    if goog_result:
        goog_name = goog_result[0]
        print(f"GOOG Name: {repr(goog_name)}")
        
        # Find the problematic character
        for i, char in enumerate(goog_name):
            if char == '':  # Replacement character
                print(f"Problematic character at position {i}: '{char}' (Unicode: {ord(char)})")
                print(f"This is the Unicode Replacement Character (U+FFFD)")
                print(f"It indicates a character that couldn't be properly decoded")
    
    # Check the original GOOGL before our fix
    print("\n=== Character Encoding Analysis ===")
    print("The character is the Unicode Replacement Character (U+FFFD)")
    print("It appears when:")
    print("1. Text was stored with wrong encoding")
    print("2. Database was created with different character set")
    print("3. Data was imported from file with encoding issues")
    
    conn.close()

def show_encoding_differences():
    print("\n=== Why Web App Shows Different Data ===")
    print("1. Database Query: Shows raw stored data with characters")
    print("2. Web App: May apply character encoding filters")
    print("3. Python/Flask: Often handles encoding automatically")
    print("4. Browser: May render replacement characters differently")

if __name__ == "__main__":
    analyze_character_encoding()
    show_encoding_differences()
