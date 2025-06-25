import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to download stock price data
def download_stock_data(tickers):
    stock_data = {}
    for ticker in tickers:
        stock_data[ticker] = yf.download(ticker, period="2y")
    return stock_data

tickers = ['UNH', 'BAC', 'MS', 'SCHW']
stock_data = download_stock_data(tickers)
