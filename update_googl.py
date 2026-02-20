import sqlite3

def show_googl_data():
    conn = sqlite3.connect('S&P500_Master.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Show current GOOGL data
    cursor.execute("SELECT * FROM Companies WHERE Ticker = 'GOOGL'")
    result = cursor.fetchone()
    
    if result:
        print("Current GOOGL data:")
        for key in result.keys():
            print(f"  {key}: {result[key]}")
    else:
        print("GOOGL not found in database")
    
    conn.close()

def update_googl_cell(column_name, new_value):
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    # Update the specific cell
    cursor.execute(f"UPDATE Companies SET {column_name} = ? WHERE Ticker = 'GOOGL'", (new_value,))
    conn.commit()
    
    print(f"Updated {column_name} to '{new_value}' for GOOGL")
    conn.close()

if __name__ == "__main__":
    # Show current data
    show_googl_data()
    
    print("\nTo update GOOGL data, use:")
    print("update_googl_cell('column_name', 'new_value')")
    print("\nExample:")
    print("update_googl_cell('Name', 'Alphabet Inc.')")
    print("update_googl_cell('Sector', 'Technology')")
