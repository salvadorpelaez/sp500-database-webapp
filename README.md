# S&P 500 Companies Database Web Application

A Flask-based web application for exploring and searching S&P 500 company data from an SQLite database.

## Features

- **Interactive Web Interface**: Modern, responsive design for browsing company data
- **Dynamic Database Connection**: Automatically discovers database tables and structure
- **Real-time Search**: Search across all company fields and columns
- **Statistics Dashboard**: View data counts and table information
- **Responsive Design**: Works on desktop and mobile devices

## Requirements

- Python 3.7+
- Flask
- SQLite3 (built into Python)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd "AI financial company"
```

2. Install Flask:
```bash
pip install flask
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

- **View Data**: The main page displays all companies from the database
- **Search**: Use the search bar to find companies by name, symbol, or any field
- **Reset**: Click the Reset button to clear search and view all data

## Database

The application connects to `S&P500_Master.db` SQLite database containing S&P 500 company information. The database structure is automatically detected, so the app works with any table structure.

## API Endpoints

- `GET /` - Main web interface
- `GET /api/companies` - Returns all companies (limited to 100 records)
- `GET /api/search?q=<query>` - Search companies by query string

## Project Structure

```
AI financial company/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main web interface
├── S&P500_Master.db   # SQLite database
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Development

To run in development mode with auto-reload:
```bash
flask --app app run --debug
```

## License

This project is open source and available under the MIT License.
