import requests

# Test the API endpoint
try:
    response = requests.get('http://127.0.0.1:5000/api/companies')
    data = response.json()
    
    print(f"Total companies returned: {len(data['companies'])}")
    
    # Check all companies with classification data
    print('\nAll companies with classification:')
    classified_companies = []
    for i, company in enumerate(data['companies']):
        if company.get('classification'):
            classified_companies.append(company)
            print(f"  {i+1}. {company['ticker']} - {company['name']} - Classification: '{company['classification']}'")
    
    print(f'\nCompanies with classification in API response: {len(classified_companies)}')
    
except Exception as e:
    print(f"Error: {e}")
