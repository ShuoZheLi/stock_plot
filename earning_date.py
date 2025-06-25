import requests
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import matplotlib.pyplot as plt

# Constants
API_KEY = 'cqbmjo1r01qvu0k06q1gcqbmjo1r01qvu0k06q20'
ALPHAVANTAGE_API_KEY = "8I36CUUIYQNJE4XY"
EARNINGS_DATE = '2024-07-19'

# Define the date range (past 2 years)
end_date = datetime.now().replace(tzinfo=None)
start_date = (end_date - timedelta(days=3*365)).replace(tzinfo=None)

# Function to fetch earnings release data
def fetch_earnings(api_key, date):
    url = f'https://finnhub.io/api/v1/calendar/earnings?from={date}&to={date}&token={api_key}'
    response = requests.get(url)
    data = response.json()
    
    # Check the structure of the returned data
    if 'earningsCalendar' in data:
        return data['earningsCalendar']
    else:
        print("Unexpected data structure:", data)
        return []

# Function to fetch market cap data
def fetch_market_cap(api_key, symbol):
    url = f'https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=marketCapitalization&token={api_key}'
    response = requests.get(url)
    data = response.json()
    
    # Check the structure of the returned data
    if 'metric' in data and 'marketCapitalization' in data['metric']:
        return data['metric']['marketCapitalization']
    else:
        print(f"Unexpected data structure for {symbol}:", data)
        return None

# def get_earnings_release_dates(ticker, start_date, end_date):
#     stock = yf.Ticker(ticker)
#     earnings_dates = stock.earnings_dates
#     earnings_dates.index = earnings_dates.index.tz_convert(None)  # Convert to tz-naive
#     earnings_dates = earnings_dates.loc[(earnings_dates.index >= start_date) & (earnings_dates.index <= end_date)]
#     return earnings_dates

def get_eps_surprise(symbol, api_key, start_date, end_date):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # import pdb; pdb.set_trace()
    
    if 'quarterlyEarnings' in data:
        earnings_data = data['quarterlyEarnings']
        eps_surprises = []

        for quarter in earnings_data:
            if 'surprise' in quarter and 'surprisePercentage' in quarter:
                eps_surprises.append({
                    'date': quarter['reportedDate'],
                    'actualEPS': quarter['reportedEPS'],
                    'estimatedEPS': quarter['estimatedEPS'],
                    'epsSurprise': quarter['surprise'],
                    'epsSurprisePercentage': quarter['surprisePercentage']
                })

        df = pd.DataFrame(eps_surprises)
        df['date'] = pd.to_datetime(df['date'])
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        df.set_index('date', inplace=True)
        return df
    else:
        return pd.DataFrame()

def plot_stock_with_earnings(ticker, stock_data, earnings_data):
    plt.figure(figsize=(14, 7))
    
    # Ensure the dates are sorted
    stock_data = stock_data.sort_index()
    earnings_data = earnings_data.sort_index()
    
    plt.plot(stock_data.index, stock_data['Close'], label=f'{ticker} Stock Price')
    
    for date, row in earnings_data.iterrows():
        if row['epsSurprisePercentage'] == 'None':
            continue
        color = 'green' if float(row['epsSurprisePercentage']) > 0 else 'red'
        plt.axvline(x=date, color=color, linestyle='--')
        plt.text(date, stock_data['Close'].max(), f'EPS\n{float(row["epsSurprisePercentage"]):.2f}%', 
                 rotation=0, verticalalignment='bottom', horizontalalignment='center', 
                 color=color, fontweight='bold')
    
    plt.title(f'{ticker} Stock Price and Earnings Surprises')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)  # Positioning the legend at the bottom
    
    # Save the plot before showing it
    plt.savefig(f'{ticker}_stock_price.png')
    plt.show()




def download_stock_data(tickers):

    end_date = datetime.now().replace(tzinfo=None) - timedelta(days=3*365)
    start_date = (end_date - timedelta(days=3*365)).replace(tzinfo=None)

    stock_data = {}
    for ticker in tickers:
        stock_data[ticker] = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Main logic
def main():
    # earnings_data = fetch_earnings(API_KEY, EARNINGS_DATE)
    # company_market_caps = []

    # for company in earnings_data:
    #     symbol = company.get('symbol')
    #     name = company.get('name', 'Unknown')
    #     market_cap = fetch_market_cap(API_KEY, symbol)
        
    #     if market_cap is not None:
    #         company_market_caps.append({'symbol': symbol, 'market_cap': market_cap})

    # df = pd.DataFrame(company_market_caps)

    # # Sort by market cap and get top 4
    # top_companies = df.sort_values(by='market_cap', ascending=False).head(4)
    # tickers = [*top_companies.to_dict()['symbol'].values()]

    # tickers = ['UNH', 'BAC', 'MS', 'SCHW']
    tickers = ['AAPL']

    # import pdb; pdb.set_trace()

    # Create a dictionary to store the results
    earnings_dates_dict = {}

    end_date = datetime.now().replace(tzinfo=None) - timedelta(days=3*365)
    start_date = (end_date - timedelta(days=3*365)).replace(tzinfo=None)

    # Fetch earnings release dates for each ticker
    for ticker in tickers:
        earnings_dates = get_eps_surprise(ticker, ALPHAVANTAGE_API_KEY, start_date, end_date)
        earnings_dates_dict[ticker] = earnings_dates
        # import pdb; pdb.set_trace()

    # Download stock data for each ticker
    stock_data = download_stock_data(tickers)


    # Plot the stock data with earnings dates
    for ticker in tickers:
        if ticker in stock_data and ticker in earnings_dates_dict:
            plot_stock_with_earnings(ticker, stock_data[ticker], earnings_dates_dict[ticker])

if __name__ == '__main__':
    main()
