import sqlite3

def copy_nasdaq_table():
    # Connect to both databases
    source_conn = sqlite3.connect('S&P500_Master_backup.db')
    target_conn = sqlite3.connect('S&P500_Master.db')
    
    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()
    
    print("Connected to both databases")
    
    # Drop the existing NASDAQ table from target database
    print("Dropping existing NASDAQ table from target database...")
    target_cursor.execute("DROP TABLE IF EXISTS NASDAQ")
    target_conn.commit()
    
    # Get the CREATE TABLE statement from source
    print("Getting table structure from source...")
    source_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='NASDAQ'")
    create_table_sql = source_cursor.fetchone()[0]
    print(f"CREATE TABLE statement: {create_table_sql}")
    
    # Create the NASDAQ table in target database
    print("Creating NASDAQ table in target database...")
    target_cursor.execute(create_table_sql)
    target_conn.commit()
    
    # Copy all data from source to target
    print("Copying data from source to target...")
    source_cursor.execute("SELECT * FROM NASDAQ")
    rows = source_cursor.fetchall()
    
    # Get column count for INSERT statement
    source_cursor.execute("PRAGMA table_info(NASDAQ)")
    columns = source_cursor.fetchall()
    column_count = len(columns)
    
    # Create placeholders for INSERT statement
    placeholders = ','.join(['?'] * column_count)
    
    # Insert all data
    target_cursor.executemany(f"INSERT INTO NASDAQ VALUES ({placeholders})", rows)
    target_conn.commit()
    
    # Verify the copy
    target_cursor.execute("SELECT COUNT(*) FROM NASDAQ")
    target_count = target_cursor.fetchone()[0]
    
    source_cursor.execute("SELECT COUNT(*) FROM NASDAQ")
    source_count = source_cursor.fetchone()[0]
    
    print(f"Source NASDAQ table: {source_count} rows")
    print(f"Target NASDAQ table: {target_count} rows")
    
    if target_count == source_count:
        print("✅ Successfully copied NASDAQ table!")
    else:
        print("❌ Copy failed - row counts don't match")
    
    # Close connections
    source_conn.close()
    target_conn.close()
    
    print("Done!")

if __name__ == "__main__":
    copy_nasdaq_table()
