import sqlite3

conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

print("=== ENERGY SECTOR CLASSIFICATION CHECK ===")
cursor.execute("SELECT Ticker, Name, Classification FROM Companies WHERE Sector = 'Energy'")
energy_companies = cursor.fetchall()

print(f"Total Energy companies: {len(energy_companies)}")
print("\nEnergy companies with classification:")
classified_energy = []
for company in energy_companies:
    if company[2]:  # Classification is not null/empty
        classified_energy.append(company)
        print(f"  {company[0]} - {company[1]} - Classification: '{company[2]}'")

if not classified_energy:
    print("  NONE - All Energy companies have empty classification")

print(f"\nEnergy companies with classification: {len(classified_energy)}")

print("\n=== ALL CLASSIFIED COMPANIES ===")
cursor.execute("SELECT Ticker, Name, Sector, Classification FROM Companies WHERE Classification IS NOT NULL AND Classification != ''")
all_classified = cursor.fetchall()
for company in all_classified:
    print(f"  {company[0]} - {company[1]} - Sector: {company[2]} - Classification: '{company[3]}'")

conn.close()
