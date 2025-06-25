import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def plot_aug_oct_highlight(ticker: str, years_back: int = 4):
    """
    Plot `ticker` closing price and shade:
      • July (light blue)
      • August–October (light gray)
    For the last `years_back` full calendar years.
    """
    this_year  = datetime.now().year - 4
    end_year   = this_year - 1
    start_year = end_year - (years_back - 1)

    start_date = f"{start_year}-01-01"
    end_date   = f"{end_year}-12-31"
    df = yf.download(ticker, start=start_date, end=end_date, progress=False, threads=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['Close'], label=f"{ticker} Close")

    for yr in range(start_year, end_year + 1):
        # Highlight July
        july_start = pd.Timestamp(f"{yr}-07-01")
        july_end   = pd.Timestamp(f"{yr}-07-31")
        ax.axvspan(july_start, july_end, alpha=0.15, color='blue', label='July' if yr == start_year else "")

        # Highlight Aug–Oct
        aug_start = pd.Timestamp(f"{yr}-08-01")
        oct_end   = pd.Timestamp(f"{yr}-10-31")
        ax.axvspan(aug_start, oct_end, alpha=0.20, color='grey', label='Aug–Oct' if yr == start_year else "")

    ax.set_title(f"{ticker}: July and Aug–Oct highlighted ({start_year}–{end_year})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    plt.tight_layout()
    plt.show()

# Example call
plot_aug_oct_highlight("QQQ", years_back=4)
