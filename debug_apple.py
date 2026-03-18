import requests

# Test a specific company that should have classification
try:
    response = requests.get('http://127.0.0.1:5000/api/companies')
    data = response.json()
    
    # Find Apple (AAPL) which should have VALUE classification
    apple = None
    for company in data['companies']:
        if company['ticker'] == 'AAPL':
            apple = company
            break
    
    if apple:
        print(f"Apple data from API:")
        print(f"  Ticker: '{apple['ticker']}'")
        print(f"  Name: '{apple['name']}'")
        print(f"  Sector: '{apple['sector']}'")
        print(f"  Sub_Sector: '{apple['sub_sector']}'")
        print(f"  Classification: '{apple.get('classification')}'")
        print(f"  Classification type: {type(apple.get('classification'))}")
        print(f"  Classification length: {len(apple.get('classification', ''))}")
    else:
        print("Apple not found in API response")
        
except Exception as e:
    print(f"Error: {e}")
