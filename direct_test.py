import sqlite3

# Direct database test
conn = sqlite3.connect('S&P500_Master.db')
cursor = conn.cursor()

print("=== DIRECT DATABASE QUERY ===")
cursor.execute("SELECT Ticker, Name, Classification FROM Companies WHERE Classification IS NOT NULL AND Classification != '' LIMIT 5")
results = cursor.fetchall()

for i, result in enumerate(results):
    print(f"{i+1}. Ticker: {result[0]}, Name: {result[1]}, Classification: '{result[2]}'")

print(f"\nTotal companies with classification: {len(results)}")

conn.close()

# Test the API response structure
print("\n=== API RESPONSE TEST ===")
import requests
try:
    response = requests.get('http://127.0.0.1:5000/api/companies')
    data = response.json()
    
    # Find companies with classification
    classified = [c for c in data['companies'] if c.get('classification')]
    
    print(f"API returned {len(data['companies'])} companies")
    print(f"Companies with classification in API: {len(classified)}")
    
    for company in classified[:3]:
        print(f"  {company['ticker']}: classification='{company.get('classification')}' (type: {type(company.get('classification'))})")
        
except Exception as e:
    print(f"API Error: {e}")
