import sqlite3

def verify_nyse_table():
    conn = sqlite3.connect('S&P500_Master.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("🔍 NYSE Table Verification")
    print("=" * 60)
    
    # Check if NYSE table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='NYSE';")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print("✅ NYSE table exists in database")
        
        # Check table structure
        cursor.execute("PRAGMA table_info(NYSE);")
        columns = cursor.fetchall()
        print(f"\n📋 Table structure ({len(columns)} columns):")
        for col in columns:
            print(f"   {col[1]} ({col[2]})")
        
        # Check row count
        cursor.execute("SELECT COUNT(*) FROM NYSE;")
        total_rows = cursor.fetchone()[0]
        print(f"\n📊 Total rows: {total_rows}")
        
        # Check populated data
        cursor.execute("SELECT COUNT(*) FROM NYSE WHERE ISIN_Code IS NOT NULL;")
        with_isin = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM NYSE WHERE Sector IS NOT NULL;")
        with_sector = cursor.fetchone()[0]
        
        print(f"📈 Data population:")
        print(f"   With ISIN_Code: {with_isin} ({with_isin/total_rows*100:.1f}%)")
        print(f"   With Sector: {with_sector} ({with_sector/total_rows*100:.1f}%)")
        
        # Show sample data
        cursor.execute("SELECT Ticker, Company_Name, ISIN_Code, Sector FROM NYSE LIMIT 5;")
        sample_data = cursor.fetchall()
        print(f"\n📝 Sample data:")
        for row in sample_data:
            ticker, company, isin, sector = row
            print(f"   {ticker}: {company} | ISIN: {isin or 'N/A'} | Sector: {sector or 'N/A'}")
        
        # Check unique sectors
        cursor.execute("SELECT DISTINCT Sector FROM NYSE WHERE Sector IS NOT NULL ORDER BY Sector;")
        sectors = cursor.fetchall()
        print(f"\n🏢 Unique sectors found: {len(sectors)}")
        for sector in sectors[:10]:  # Show first 10
            print(f"   {sector[0]}")
        if len(sectors) > 10:
            print(f"   ... and {len(sectors) - 10} more")
            
    else:
        print("❌ NYSE table not found in database")
    
    # Show all tables in database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = cursor.fetchall()
    print(f"\n📚 All tables in database:")
    for table in all_tables:
        print(f"   {table[0]}")
    
    conn.close()
    print("\n✅ Verification complete!")

if __name__ == "__main__":
    verify_nyse_table()
