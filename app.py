from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('S&P500_Master.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

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
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        companies = cursor.fetchall()
        
        # Convert to list of dictionaries
        companies_list = [dict(company) for company in companies]
        
        return jsonify({
            'table_name': table_name,
            'companies': companies_list,
            'total_count': len(companies_list)
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
        
        # Build dynamic search query
        search_conditions = []
        for col in column_names:
            search_conditions.append(f"LOWER({col}) LIKE ?")
        
        search_query = f"SELECT * FROM {table_name} WHERE {' OR '.join(search_conditions)} LIMIT 50"
        search_params = [f'%{query}%'] * len(column_names)
        
        cursor.execute(search_query, search_params)
        results = cursor.fetchall()
        
        return jsonify({
            'companies': [dict(result) for result in results],
            'query': query,
            'total_count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
