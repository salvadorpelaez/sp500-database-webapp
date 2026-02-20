import sqlite3

def fix_encoding_properly():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    # Manual fixes for each company
    fixes = {
        'GOOG': 'Alphabet Inc. (Class C)',
        'BF.B': 'Brown-Forman',
        'EL': 'Estée Lauder Companies (The)',
        'FOXA': 'Fox Corporation (Class A)',
        'FOX': 'Fox Corporation (Class B)',
        'NWSA': 'News Corp (Class A)',
        'NWS': 'News Corp (Class B)',
        'ORLY': "O'Reilly Automotive"
    }
    
    print("Fixing encoding issues manually...")
    
    for ticker, correct_name in fixes.items():
        cursor.execute('UPDATE Companies SET Name = ? WHERE Ticker = ?', (correct_name, ticker))
        print(f"✅ Fixed {ticker}: {correct_name}")
    
    conn.commit()
    print(f"\n✅ Fixed {len(fixes)} encoding issues")
    conn.close()

def show_final_results():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT Ticker, Name FROM Companies WHERE Ticker IN (?, ?, ?, ?, ?, ?, ?, ?)', 
                  ('GOOG', 'BF.B', 'EL', 'FOXA', 'FOX', 'NWSA', 'NWS', 'ORLY'))
    
    print("\n=== Final Fixed Company Names ===")
    for ticker, name in cursor.fetchall():
        print(f"{ticker}: {name}")
    
    conn.close()

if __name__ == "__main__":
    fix_encoding_properly()
    show_final_results()
