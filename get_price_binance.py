from binance import Client
import pandas as pd
from datetime import datetime
import time

# Initialize Binance client with your credentials
client = Client('api_key', 
               'api_secret')

def get_btc_closing_price(timestamp):
    """
    Fetch BTC closing price from Binance for a specific timestamp
    """
    try:
        # Convert timestamp to milliseconds
        ts = int(timestamp.timestamp() * 1000)
        
        # Get klines (candlestick) data
        # Fetch 1-hour candlestick for the specific timestamp
        klines = client.get_historical_klines(
            "BTCUSDT",
            Client.KLINE_INTERVAL_1HOUR,
            str(ts),
            str(ts + 3600000)  # Add 1 hour in milliseconds
        )
        
        if klines:
            # Closing price is the 4th element in the kline data
            return float(klines[0][4])
        return None
        
    except Exception as e:
        print(f"Error fetching price for {timestamp}: {str(e)}")
        return None

# Read the dataset
df = pd.read_csv('cleaned_aggregated_telegram_data.csv')

# Convert 'hour' column to datetime
df['hour'] = pd.to_datetime(df['hour'])

# Create new column for BTC prices
df['BTC_closing_price'] = None

# Counter for rate limiting
request_count = 0

# Process each row
for index, row in df.iterrows():
    # Rate limiting: pause every 10 requests
    if request_count >= 10:
        print("Pausing for rate limit...")
        time.sleep(1)
        request_count = 0
        
    closing_price = get_btc_closing_price(row['hour'])
    if closing_price is not None:
        df.at[index, 'BTC_closing_price'] = closing_price
        print(f"Successfully fetched price for {row['hour']}: ${closing_price:.2f}")
    
    request_count += 1
    # Small delay between requests
    time.sleep(0.1)

# Remove any duplicates
df.drop_duplicates(subset=['hour'], keep='first', inplace=True)

# Save the updated dataset
df.to_csv('telegram_data_with_btc_prices.csv', index=False)

# Print summary
print("\nProcessing Summary:")
print(f"Total rows processed: {len(df)}")
print(f"Successful price fetches: {df['BTC_closing_price'].notna().sum()}")
print(f"Missing prices: {df['BTC_closing_price'].isna().sum()}")

# Display sample of results
print("\nSample of results:")
print(df[['hour', 'BTC_closing_price']].head())
