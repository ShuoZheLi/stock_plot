import yfinance as yf
import matplotlib.pyplot as plt
import requests
import pandas as pd

# Function to get earnings data from finnhub.io
def get_earnings_data(api_key, symbol):
    url = f"https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={api_key}"
    response = requests.get(url)
    data = response.json()
    earnings_data = {}
    for entry in data:
        date = entry['period']
        revenue_surprise = entry.get('revenueSurprise', 0)  # Revenue Surprise in dollars
        revenue_actual = entry.get('revenueActual', 1)      # Actual Revenue in dollars
        revenue_expected = entry.get('revenueEstimate', 1)  # Estimated Revenue in dollars
        eps_surprise = entry.get('epsSurprise', 0)          # EPS Surprise in dollars
        eps_actual = entry.get('epsActual', 1)              # Actual EPS
        eps_expected = entry.get('epsEstimate', 1)          # Estimated EPS
        
        import pdb; pdb.set_trace()

        revenue_surprise_percent = (revenue_surprise / revenue_expected) * 100 if revenue_expected != 0 else 0
        eps_surprise_percent = (eps_surprise / eps_expected) * 100 if eps_expected != 0 else 0
        
        earnings_data[date] = (revenue_surprise_percent, eps_surprise_percent)
    return earnings_data

# Function to plot stock prices and annotate with earnings data
def plot_stock_with_earnings(ticker, stock_data, earnings_data):
    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Close'], label=f'{ticker} Stock Price')
    
    for date, (revenue_surprise, eps_surprise) in earnings_data.items():
        plt.axvline(x=pd.to_datetime(date), color='red', linestyle='--')
        plt.text(pd.to_datetime(date), stock_data['Close'].max(), f'Rev: {revenue_surprise:.2f}%\nEPS: {eps_surprise:.2f}%', rotation=0, verticalalignment='bottom')
    
    plt.title(f'{ticker} Stock Price and Earnings Surprises')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

# Main function to fetch data and plot
def main():
    tickers = ['UNH', 'BAC', 'MS', 'SCHW']
    api_key = 'cqb3kjpr01qmfd85n45gcqb3kjpr01qmfd85n460'  # Replace with your finnhub.io API key
    
    for ticker in tickers:
        # Fetch stock data
        stock_data = yf.download(ticker, start='2022-01-01', end='2024-12-31')
        
        # Fetch earnings data
        earnings_data = get_earnings_data(api_key, ticker)
        
        # Plot stock data with earnings annotations
        plot_stock_with_earnings(ticker, stock_data, earnings_data)

# Run the main function
if __name__ == "__main__":
    main()
