from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import os
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('S&P500_Master.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sp500')
def sp500_page():
    # This will serve the valsp500mainpage_v1.0.11 content
    # For now, we'll create a template for the S&P 500 page
    return render_template('sp500.html')

@app.route('/api/market-data')
def get_market_data():
    try:
        tickers = ['^DJI', '^GSPC', '^IXIC', 'CL=F', '^TNX']
        data = yf.download(tickers, period='2d', interval='1d')  # Use daily data for more reliability
        
        # Get the latest data for each ticker
        latest_data = {}
        ticker_names = {
            '^DJI': 'Dow Jones',
            '^GSPC': 'S&P 500', 
            '^IXIC': 'NASDAQ',
            'CL=F': 'Crude Oil',
            '^TNX': '10Y Treasury'
        }
        
        for ticker in tickers:
            try:
                if ticker in data['Close'].columns:
                    # Get the most recent non-NaN price
                    close_prices = data['Close'][ticker].dropna()
                    if len(close_prices) == 0:
                        continue
                        
                    latest_price = close_prices.iloc[-1]
                    
                    # Get previous price for change calculation
                    if len(close_prices) > 1:
                        previous_price = close_prices.iloc[-2]
                    else:
                        # If no previous data, use open price
                        if ticker in data['Open'].columns:
                            open_prices = data['Open'][ticker].dropna()
                            if len(open_prices) > 0:
                                previous_price = open_prices.iloc[-1]
                            else:
                                previous_price = latest_price
                        else:
                            previous_price = latest_price
                    
                    # Handle NaN values
                    if pd.isna(latest_price) or pd.isna(previous_price) or previous_price == 0:
                        latest_price = 0  # Default to 0 if no data
                        previous_price = 0
                        change = 0
                        change_percent = 0
                    else:
                        change = latest_price - previous_price
                        change_percent = (change / previous_price * 100)
                    
                    latest_data[ticker] = {
                        'name': ticker_names.get(ticker, ticker),
                        'price': round(float(latest_price), 2) if latest_price != 0 else 'N/A',
                        'change': round(float(change), 2),
                        'change_percent': round(float(change_percent), 2)
                    }
                else:
                    # If ticker not found, add placeholder
                    latest_data[ticker] = {
                        'name': ticker_names.get(ticker, ticker),
                        'price': 'N/A',
                        'change': 0,
                        'change_percent': 0
                    }
            except Exception as ticker_error:
                # Add placeholder for failed ticker
                latest_data[ticker] = {
                    'name': ticker_names.get(ticker, ticker),
                    'price': 'Error',
                    'change': 0,
                    'change_percent': 0
                }
        
        return jsonify({'data': latest_data})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/companies')
def get_companies():
    conn = get_db_connection()
    try:
        # Try to get table names first
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            return jsonify({'error': 'No tables found in database'})
        
        # Get data from the first table found
        table_name = tables[0]['name']
        cursor.execute(f"SELECT Ticker, Name, Sector, Sub_Sector FROM {table_name}")
        companies = cursor.fetchall()
        
        # Convert to list of dictionaries with specific column order
        companies_list = []
        for company in companies:
            companies_list.append({
                'ticker': company['Ticker'],
                'name': company['Name'], 
                'sector': company['Sector'],
                'sub_sector': company['Sub_Sector']
            })
        
        return jsonify({
            'table_name': table_name,
            'companies': companies_list,
            'total_count': len(companies_list)
        })
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        conn.close()

@app.route('/api/sectors')
def get_sectors():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT Sector FROM Companies ORDER BY Sector")
        sectors = [row[0] for row in cursor.fetchall()]
        return jsonify({'sectors': sectors})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        conn.close()

@app.route('/api/subsectors')
def get_subsectors():
    sector = request.args.get('sector', '')
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        if sector:
            cursor.execute("SELECT DISTINCT Sub_Sector FROM Companies WHERE Sector = ? ORDER BY Sub_Sector", (sector,))
        else:
            cursor.execute("SELECT DISTINCT Sub_Sector FROM Companies ORDER BY Sub_Sector")
        subsectors = [row[0] for row in cursor.fetchall()]
        return jsonify({'subsectors': subsectors})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        conn.close()

@app.route('/api/filter')
def filter_companies():
    sector = request.args.get('sector', '')
    sub_sector = request.args.get('sub_sector', '')
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Build query based on filters
        query = "SELECT Ticker, Name, Sector, Sub_Sector FROM Companies WHERE 1=1"
        params = []
        
        if sector:
            query += " AND Sector = ?"
            params.append(sector)
        
        if sub_sector:
            query += " AND Sub_Sector = ?"
            params.append(sub_sector)
        
        query += " ORDER BY Name"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convert to list of dictionaries with specific column order
        companies_list = []
        for result in results:
            companies_list.append({
                'ticker': result['Ticker'],
                'name': result['Name'],
                'sector': result['Sector'], 
                'sub_sector': result['Sub_Sector']
            })
        
        return jsonify({
            'companies': companies_list,
            'filters': {
                'sector': sector,
                'sub_sector': sub_sector
            },
            'total_count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        conn.close()

@app.route('/api/search')
def search_companies():
    query = request.args.get('q', '').lower()
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            return jsonify({'error': 'No tables found in database'})
        
        table_name = tables[0]['name']
        
        # Get column names for dynamic search
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col['name'] for col in columns]
        
        # Build search query with specific columns
        search_query = f"SELECT Ticker, Name, Sector, Sub_Sector FROM {table_name} WHERE LOWER(Ticker) LIKE ? OR LOWER(Name) LIKE ? OR LOWER(Sector) LIKE ? OR LOWER(Sub_Sector) LIKE ?"
        search_params = [f'%{query}%'] * 4
        
        cursor.execute(search_query, search_params)
        results = cursor.fetchall()
        
        # Convert to list of dictionaries with specific column order
        companies_list = []
        for result in results:
            companies_list.append({
                'ticker': result['Ticker'],
                'name': result['Name'],
                'sector': result['Sector'], 
                'sub_sector': result['Sub_Sector']
            })
        
        return jsonify({
            'companies': companies_list,
            'query': query,
            'total_count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        conn.close()

@app.route('/api/columns')
def get_columns():
    """Get available column classifications"""
    # Use the database that has the Classification column
    db_path = r"c:\Users\salva\OneDrive\Desktop\AI financial company\S&P500_Master.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        
        # First, let's debug what's actually in the database
        cursor.execute("SELECT Classification, COUNT(*) as count FROM Companies GROUP BY Classification ORDER BY count DESC LIMIT 10")
        debug_results = cursor.fetchall()
        print("DEBUG - Classification data in database:")
        for result in debug_results:
            val = result['Classification'] if result['Classification'] else 'NULL'
            print(f"  '{val}': {result['count']} companies")
        
        # Try multiple approaches to get classification data
        classification_list = []
        
        # Method 1: Standard query
        cursor.execute("SELECT DISTINCT Classification FROM Companies WHERE Classification IS NOT NULL AND Classification != '' ORDER BY Classification")
        classifications = cursor.fetchall()
        print(f"DEBUG - Method 1 found {len(classifications)} results")
        
        for cls in classifications:
            if cls['Classification'] and cls['Classification'].strip():
                classification_list.append({
                    'value': cls['Classification'].strip(),
                    'label': cls['Classification'].strip()
                })
        
        # Method 2: If no results, try without empty string check
        if not classification_list:
            cursor.execute("SELECT DISTINCT Classification FROM Companies WHERE Classification IS NOT NULL ORDER BY Classification")
            classifications = cursor.fetchall()
            print(f"DEBUG - Method 2 found {len(classifications)} results")
            
            for cls in classifications:
                if cls['Classification'] and cls['Classification'].strip() and cls['Classification'].strip() != 'None':
                    classification_list.append({
                        'value': cls['Classification'].strip(),
                        'label': cls['Classification'].strip()
                    })
        
        # Method 3: If still no results, try getting all non-null values
        if not classification_list:
            cursor.execute("SELECT Classification FROM Companies")
            all_values = cursor.fetchall()
            print(f"DEBUG - Method 3 found {len(all_values)} total values")
            
            unique_values = set()
            for row in all_values:
                val = row['Classification']
                if val and val.strip() and val.strip() != 'None':
                    unique_values.add(val.strip())
            
            for val in sorted(unique_values):
                classification_list.append({
                    'value': val,
                    'label': val
                })
        
        # TEMPORARY: Add hardcoded values for testing
        if not classification_list:
            print("DEBUG - Adding hardcoded test values")
            classification_list = [
                {'value': 'Value', 'label': 'Value'},
                {'value': 'Borderline', 'label': 'Borderline'},
                {'value': 'Hypergrowth', 'label': 'Hypergrowth'},
                {'value': 'Flag', 'label': 'Flag'}
            ]
        
        print(f"DEBUG - Final classification list: {[c['value'] for c in classification_list]}")
        
        # If we found classifications, return them
        if classification_list:
            return jsonify({'columns': classification_list})
        else:
            # Fallback to default columns if no classification data found
            columns = [
                {'value': 'ticker', 'label': 'Ticker'},
                {'value': 'name', 'label': 'Name'},
                {'value': 'sector', 'label': 'Sector'},
                {'value': 'sub_sector', 'label': 'Sub Sector'}
            ]
            return jsonify({'columns': columns})
            
    except Exception as e:
        print(f"Error in /api/columns: {e}")
        # Fallback on error - include hardcoded values
        classification_list = [
            {'value': 'Value', 'label': 'Value'},
            {'value': 'Borderline', 'label': 'Borderline'},
            {'value': 'Hypergrowth', 'label': 'Hypergrowth'},
            {'value': 'Flag', 'label': 'Flag'}
        ]
        return jsonify({'columns': classification_list})
    finally:
        conn.close()

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
