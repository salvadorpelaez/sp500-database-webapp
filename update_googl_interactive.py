import sqlite3

def show_googl_data():
    conn = sqlite3.connect('S&P500_Master.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
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
    
    # Validate column name
    valid_columns = ['ID', 'Ticker', 'Name', 'Sector', 'Sub_Sector', 'Headquarters_Location', 'Date_Added', 'CIK', 'Founded']
    if column_name not in valid_columns:
        print(f"Invalid column name. Valid columns: {valid_columns}")
        return False
    
    cursor.execute(f"UPDATE Companies SET {column_name} = ? WHERE Ticker = 'GOOGL'", (new_value,))
    conn.commit()
    
    print(f"✅ Updated {column_name} to '{new_value}' for GOOGL")
    conn.close()
    return True

if __name__ == "__main__":
    print("=== GOOGL Database Update Tool ===\n")
    
    # Show current data
    show_googl_data()
    
    print("\n=== Update Options ===")
    print("1. Update Name")
    print("2. Update Sector") 
    print("3. Update Sub_Sector")
    print("4. Update Headquarters_Location")
    print("5. Custom column update")
    print("6. Just show current data")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == '1':
        new_name = input("Enter new name: ").strip()
        update_googl_cell('Name', new_name)
    elif choice == '2':
        new_sector = input("Enter new sector: ").strip()
        update_googl_cell('Sector', new_sector)
    elif choice == '3':
        new_sub_sector = input("Enter new sub sector: ").strip()
        update_googl_cell('Sub_Sector', new_sub_sector)
    elif choice == '4':
        new_hq = input("Enter new headquarters location: ").strip()
        update_googl_cell('Headquarters_Location', new_hq)
    elif choice == '5':
        column = input("Enter column name: ").strip()
        value = input("Enter new value: ").strip()
        update_googl_cell(column, value)
    elif choice == '6':
        print("\nShowing current data only.")
    else:
        print("Invalid choice.")
    
    # Show updated data
    if choice in ['1', '2', '3', '4', '5']:
        print("\n=== Updated GOOGL Data ===")
        show_googl_data()
