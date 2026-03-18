import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

# Check Energy companies
cursor.execute("SELECT Ticker, Name, Sector, Classification FROM Companies WHERE Sector = 'Energy'")
energy_companies = cursor.fetchall()
print(f"Energy companies ({len(energy_companies)}):")
for result in energy_companies:
    print(f"  {result[0]} - {result[1]} - Classification: {result[3]}")

print()

# Check VALUE companies  
cursor.execute("SELECT Ticker, Name, Sector, Classification FROM Companies WHERE Classification = 'VALUE'")
value_companies = cursor.fetchall()
print(f"VALUE companies ({len(value_companies)}):")
for result in value_companies:
    print(f"  {result[0]} - {result[1]} - Sector: {result[3]}")

print()

# Check all companies with classifications
cursor.execute("SELECT Ticker, Name, Sector, Classification FROM Companies WHERE Classification IS NOT NULL AND Classification != ''")
all_classified = cursor.fetchall()
print(f"All companies with classifications ({len(all_classified)}):")
for result in all_classified:
    print(f"  {result[0]} - {result[1]} - Sector: {result[2]} - Classification: {result[3]}")

conn.close()
