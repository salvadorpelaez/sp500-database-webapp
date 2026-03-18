"""
populate_nyse.py
--------------
Reads NYSE companies from CSV file, fetches ISIN and Sector from Yahoo Finance,
and populates the NYSE table in SQLite database.

Setup:
    pip install pandas yfinance

Usage:
    python populate_nyse.py

CSV File Format:
    - Must have columns: Ticker, Company_Name
    - Place CSV file in the same directory as this script
    - Recommended filename: nyse_companies.csv

Notes:
    - Yahoo Finance rate-limits aggressively — script adds a
      small delay between calls to avoid getting blocked
    - Some tickers may return None for ISIN or Sector (e.g.
      foreign-listed or delisted stocks) — these are skipped
      and logged to failed_nyse_tickers.txt
    - Safe to re-run — only updates rows where ISIN_Code or
      Sector is still NULL
"""

import sqlite3
import pandas as pd
import time
import yfinance as yf
import os

# ── Config ──
DB_PATH = "S&P500_Master.db"
TABLE = "NYSE"
CSV_FILE = "nyse_companies.csv"  # Change this if your CSV has a different name
DELAY = 1.5  # seconds between API calls — keep at 1.0+ to avoid rate limits

# ── Step 1: Create NYSE table if it doesn't exist ──
def create_nyse_table(conn):
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            Ticker TEXT PRIMARY KEY,
            Company_Name TEXT,
            ISIN_Code TEXT,
            Sector TEXT
        )
    """)
    
    # Create indexes
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE}_ticker ON {TABLE}(Ticker)")
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE}_sector ON {TABLE}(Sector)")
    
    conn.commit()
    print(f"Created {TABLE} table (if it didn't exist)")

# ── Step 2: Load CSV and insert basic data ──
def load_csv_data(conn):
    if not os.path.exists(CSV_FILE):
        print(f"❌ CSV file not found: {CSV_FILE}")
        print(f"Please place your NYSE CSV file in the current directory as '{CSV_FILE}'")
        return False
    
    try:
        df = pd.read_csv(CSV_FILE)
        
        # Check required columns
        required_columns = ['Ticker', 'Company_Name']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns in CSV: {missing_columns}")
            print(f"Found columns: {list(df.columns)}")
            return False
        
        print(f"✅ Loaded CSV with {len(df)} companies")
        print(f"CSV columns: {list(df.columns)}")
        
        # Insert basic data (Ticker and Company_Name)
        cursor = conn.cursor()
        inserted_count = 0
        
        for _, row in df.iterrows():
            ticker = str(row['Ticker']).strip().upper()
            company_name = str(row['Company_Name']).strip()
            
            # Insert or update the record
            cursor.execute(f"""
                INSERT OR REPLACE INTO {TABLE} (Ticker, Company_Name, ISIN_Code, Sector)
                VALUES (?, ?, NULL, NULL)
            """, (ticker, company_name))
            inserted_count += 1
        
        conn.commit()
        print(f"✅ Inserted/updated {inserted_count} companies in {TABLE} table")
        return True
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False

# ── Step 3: Fetch tickers that still need ISIN/Sector data ──
def get_tickers_to_update(conn):
    cursor = conn.cursor()
    rows = cursor.execute(f"""
        SELECT Ticker FROM {TABLE}
        WHERE ISIN_Code IS NULL OR Sector IS NULL
        ORDER BY Ticker
    """).fetchall()
    return [row[0] for row in rows]

# ── Step 4: Fetch ISIN + Sector from Yahoo Finance ──
def fetch_yahoo_data(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        
        # ISIN — direct property on Ticker object
        isin = None
        try:
            isin = t.isin
            if isin == "None" or isin == "":
                isin = None
        except Exception:
            isin = None
        
        # Sector — from the info dict
        sector = None
        try:
            info = t.info
            sector = info.get("sector", None)
        except Exception:
            sector = None
        
        return isin, sector
        
    except Exception as e:
        print(f"  ERROR fetching {ticker_symbol}: {e}")
        return None, None

# ── Step 5: Write results back to SQLite ──
def update_row(conn, ticker, isin, sector):
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {TABLE}
        SET ISIN_Code = COALESCE(ISIN_Code, ?),
            Sector    = COALESCE(Sector, ?)
        WHERE Ticker = ?
    """, (isin, sector, ticker))
    conn.commit()

# ── Main ──
def main():
    print("=" * 60)
    print("🏦 NYSE Table Population Script")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to {DB_PATH}")
    
    # Create table
    create_nyse_table(conn)
    
    # Load CSV data
    if not load_csv_data(conn):
        conn.close()
        return
    
    # Get tickers to update
    tickers = get_tickers_to_update(conn)
    total = len(tickers)
    print(f"\nFound {total} ticker(s) needing ISIN or Sector data.")
    
    if total == 0:
        print("Nothing to update — all rows already populated.")
        conn.close()
        return
    
    # Process tickers
    failed = []
    
    for i, ticker in enumerate(tickers, start=1):
        print(f"[{i}/{total}] {ticker} ... ", end="", flush=True)
        
        isin, sector = fetch_yahoo_data(ticker)
        
        if isin or sector:
            update_row(conn, ticker, isin, sector)
            print(f"ISIN={isin or 'n/a'}  Sector={sector or 'n/a'}")
        else:
            failed.append(ticker)
            print("no data returned — skipped")
        
        time.sleep(DELAY)
    
    # Summary
    succeeded = total - len(failed)
    print(f"\n" + "=" * 60)
    print(f"📊 SUMMARY:")
    print(f"   Total processed: {total}")
    print(f"   Successfully updated: {succeeded}")
    print(f"   Failed: {len(failed)}")
    
    if failed:
        with open("failed_nyse_tickers.txt", "w") as f:
            f.write("\n".join(failed))
        print(f"   Failed tickers saved to: failed_nyse_tickers.txt")
    
    # Show final table stats
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE}")
    total_rows = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE ISIN_Code IS NOT NULL")
    with_isin = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE Sector IS NOT NULL")
    with_sector = cursor.fetchone()[0]
    
    print(f"\n📈 Final {TABLE} table stats:")
    print(f"   Total companies: {total_rows}")
    print(f"   With ISIN: {with_isin}")
    print(f"   With Sector: {with_sector}")
    
    conn.close()
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
