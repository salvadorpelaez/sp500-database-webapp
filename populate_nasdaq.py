"""
populate_nasdaq.py
------------------
Reads all Ticker values from your NASDAQ table in SQLite,
fetches ISIN and Sector from Yahoo Finance (yfinance),
and writes them back to the table.
 
Setup:
    pip install yfinance
 
Usage:
    python populate_nasdaq.py
 
Notes:
    - Run this ONCE to do the initial bulk population
    - Yahoo Finance rate-limits aggressively — script adds a
      small delay between calls to avoid getting blocked
    - Some tickers may return None for ISIN or Sector (e.g.
      foreign-listed or delisted stocks) — these are skipped
      and logged to failed_tickers.txt
    - Safe to re-run — only updates rows where ISIN_Code or
      Sector is still NULL
"""
 
import sqlite3
import time
import yfinance as yf
 
# ── Config ── update DB_PATH to match your project
DB_PATH = "S&P500_Master_backup.db"   # e.g. "valerious.db" or "sp500.db"
TABLE   = "NASDAQ"
DELAY   = 1.5   # seconds between API calls — keep at 1.0+ to avoid rate limits
 
# ── Step 1: Add columns if they don't exist yet ──
def add_columns_if_missing(conn):
    cursor = conn.cursor()
    existing = [row[1] for row in cursor.execute(f"PRAGMA table_info({TABLE})")]
    if "ISIN_Code" not in existing:
        print("Adding ISIN_Code column...")
        cursor.execute(f"ALTER TABLE {TABLE} ADD COLUMN ISIN_Code TEXT")
    if "Sector" not in existing:
        print("Adding Sector column...")
        cursor.execute(f"ALTER TABLE {TABLE} ADD COLUMN Sector TEXT")
    conn.commit()
 
# ── Step 2: Fetch tickers that still need data ──
def get_tickers_to_update(conn):
    cursor = conn.cursor()
    rows = cursor.execute(f"""
        SELECT Symbol FROM {TABLE}
        WHERE ISIN_Code IS NULL OR Sector IS NULL
        ORDER BY Symbol
    """).fetchall()
    return [row[0] for row in rows]
 
# ── Step 3: Fetch ISIN + Sector from Yahoo Finance ──
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
            info   = t.info
            sector = info.get("sector", None)
        except Exception:
            sector = None
 
        return isin, sector
 
    except Exception as e:
        print(f"  ERROR fetching {ticker_symbol}: {e}")
        return None, None
 
# ── Step 4: Write results back to SQLite ──
def update_row(conn, ticker, isin, sector):
    conn.execute(f"""
        UPDATE {TABLE}
        SET ISIN_Code = COALESCE(ISIN_Code, ?),
            Sector    = COALESCE(Sector, ?)
        WHERE Symbol = ?
    """, (isin, sector, ticker))
    conn.commit()
 
# ── Main ──
def main():
    conn = sqlite3.connect(DB_PATH)
 
    print(f"Connected to {DB_PATH}")
    add_columns_if_missing(conn)
 
    tickers = get_tickers_to_update(conn)
    total   = len(tickers)
    print(f"Found {total} ticker(s) needing ISIN or Sector data.\n")
 
    if total == 0:
        print("Nothing to update — all rows already populated.")
        conn.close()
        return
 
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
 
    # ── Summary ──
    succeeded = total - len(failed)
    print(f"\nDone. {succeeded}/{total} tickers updated.")
 
    if failed:
        with open("failed_tickers.txt", "w") as f:
            f.write("\n".join(failed))
        print(f"{len(failed)} tickers had no data — saved to failed_tickers.txt")
 
    conn.close()
 
if __name__ == "__main__":
    main()
