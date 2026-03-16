import pandas as pd
import requests
import os
from datetime import datetime

def download_equities_list():
    """
    Download complete equities list from Alpha Vantage and save as CSV
    """
    # Get API key from environment variable or use demo
    API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY', 'demo')
    
    print(f"Using API Key: {API_KEY[:8]}..." if API_KEY != 'demo' else "Using demo API key")
    
    # Define the URL for listing status
    CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}'
    
    try:
        print("Downloading equities list from Alpha Vantage...")
        
        # Download and load into DataFrame
        df = pd.read_csv(CSV_URL)
        
        print(f"Total securities found: {len(df)}")
        
        # Filter for just Stocks (removing ETFs, etc.)
        stocks_only = df[df['assetType'] == 'Stock']
        
        print(f"Total equities (stocks only): {len(stocks_only)}")
        print(f"Columns available: {list(df.columns)}")
        
        # Display sample data
        print("\nSample equities:")
        print(stocks_only.head(10).to_string())
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"equities_list_{timestamp}.csv"
        
        # Save the complete equities list to CSV
        stocks_only.to_csv(csv_filename, index=False)
        print(f"\n✅ Equities list saved to: {csv_filename}")
        
        # Also save a version without timestamp for easy access
        latest_filename = "latest_equities_list.csv"
        stocks_only.to_csv(latest_filename, index=False)
        print(f"✅ Latest version saved to: {latest_filename}")
        
        # Display statistics
        print(f"\n📊 Statistics:")
        print(f"   Total equities: {len(stocks_only):,}")
        print(f"   Active equities: {len(stocks_only[stocks_only['status'] == 'Active']):,}")
        print(f"   Delisted equities: {len(stocks_only[stocks_only['status'] == 'Delisted']):,}")
        
        # Show exchange distribution
        if 'exchange' in stocks_only.columns:
            print(f"\n📈 Exchange Distribution:")
            exchange_counts = stocks_only['exchange'].value_counts().head(10)
            for exchange, count in exchange_counts.items():
                print(f"   {exchange}: {count:,}")
        
        return stocks_only, csv_filename
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None, None
    except pd.errors.EmptyDataError:
        print("❌ No data received from Alpha Vantage")
        return None, None
    except Exception as e:
        print(f"❌ Error downloading equities list: {e}")
        return None, None

def main():
    """Main function to download equities list"""
    print("=" * 60)
    print("🏦 Alpha Vantage Equities List Downloader")
    print("=" * 60)
    
    equities_df, filename = download_equities_list()
    
    if equities_df is not None:
        print(f"\n🎉 Successfully downloaded {len(equities_df):,} equities!")
        print(f"📁 File saved as: {filename}")
        
        # Ask if user wants to see more details
        show_details = input("\nShow detailed statistics? (y/n): ").lower()
        if show_details == 'y':
            print(f"\n📋 Detailed Info:")
            print(f"   DataFrame shape: {equities_df.shape}")
            print(f"   Memory usage: {equities_df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
            
            if 'ipoDate' in equities_df.columns:
                print(f"   IPO date range: {equities_df['ipoDate'].min()} to {equities_df['ipoDate'].max()}")
            
            if 'delistingDate' in equities_df.columns:
                delisted_count = equities_df['delistingDate'].notna().sum()
                print(f"   Companies with delisting dates: {delisted_count:,}")
    else:
        print("❌ Failed to download equities list")
        print("💡 Check your API key or internet connection")

if __name__ == "__main__":
    main()
