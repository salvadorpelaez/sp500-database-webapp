import sqlite3

def fix_encoding_issues():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    # Get all companies with encoding issues
    cursor.execute('SELECT Ticker, Name FROM Companies WHERE Name LIKE "%�%"')
    problematic_companies = cursor.fetchall()
    
    print(f"Found {len(problematic_companies)} companies with encoding issues:")
    
    for ticker, name in problematic_companies:
        print(f"\nProcessing {ticker}: {repr(name)}")
        
        # Replace the replacement character with proper characters
        fixed_name = name.replace('', '(')  # Replace with opening parenthesis
        fixed_name = fixed_name.replace('�', '(')  # Also handle the visible version
        
        # Handle specific cases
        if 'Brown' in fixed_name and 'Forman' in fixed_name:
            fixed_name = fixed_name.replace('Brown(Forman', 'Brown-Forman')
        elif 'O' in fixed_name and 'Reilly' in fixed_name:
            fixed_name = fixed_name.replace('O(Reilly', "O'Reilly")
        elif 'Est' in fixed_name and 'e Lauder' in fixed_name:
            fixed_name = fixed_name.replace('Est(e Lauder', "Estée Lauder")
        elif 'Fox Corporation' in fixed_name:
            fixed_name = fixed_name.replace('Fox Corporation(', 'Fox Corporation (')
        elif 'News Corp' in fixed_name:
            fixed_name = fixed_name.replace('News Corp(', 'News Corp (')
        elif 'Alphabet Inc' in fixed_name:
            fixed_name = fixed_name.replace('Alphabet Inc(', 'Alphabet Inc. (')
        
        # Update the database
        cursor.execute('UPDATE Companies SET Name = ? WHERE Ticker = ?', (fixed_name, ticker))
        print(f"  Fixed: {fixed_name}")
    
    conn.commit()
    print(f"\n✅ Fixed {len(problematic_companies)} encoding issues")
    conn.close()

def show_fixed_results():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    # Show the fixed companies
    cursor.execute('SELECT Ticker, Name FROM Companies WHERE Ticker IN (?, ?, ?, ?, ?, ?, ?, ?)', 
                  ('GOOG', 'BF.B', 'EL', 'FOXA', 'FOX', 'NWSA', 'NWS', 'ORLY'))
    
    print("\n=== Fixed Company Names ===")
    for ticker, name in cursor.fetchall():
        print(f"{ticker}: {name}")
    
    conn.close()

if __name__ == "__main__":
    fix_encoding_issues()
    show_fixed_results()
