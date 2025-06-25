import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the ticker symbols for the companies
tickers = ['UNH', 'BAC', 'MS', 'SCHW']

# Define the date range (past 2 years)
end_date = datetime.now().replace(tzinfo=None)
start_date = (end_date - timedelta(days=4*365)).replace(tzinfo=None)

# Function to get earnings release dates
def get_earnings_release_dates(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    earnings_dates = stock.earnings_dates
    earnings_dates.index = earnings_dates.index.tz_convert(None)  # Convert to tz-naive
    earnings_dates = earnings_dates.loc[(earnings_dates.index >= start_date) & (earnings_dates.index <= end_date)]
    return earnings_dates

# Create a dictionary to store the results
earnings_dates_dict = {}

# Fetch earnings release dates for each ticker
for ticker in tickers:
    earnings_dates = get_earnings_release_dates(ticker, start_date, end_date)
    earnings_dates_dict[ticker] = earnings_dates

import pdb; pdb.set_trace()

# Convert the dictionary to a DataFrame for better visualization
earnings_dates_df = pd.concat(earnings_dates_dict, axis=1)

# Print the DataFrame
print(earnings_dates_df)
