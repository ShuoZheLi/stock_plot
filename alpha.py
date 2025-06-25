import requests
import pandas as pd

def get_eps_surprise(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
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

        # Convert to DataFrame for better readability
        df = pd.DataFrame(eps_surprises)
        # Filter data for the past 2 years
        df['date'] = pd.to_datetime(df['date'])
        two_years_ago = pd.Timestamp.today() - pd.DateOffset(years=2)
        df = df[df['date'] >= two_years_ago]

        return df
    else:
        return pd.DataFrame()

# Example usage
symbol = "BAC"  # Replace with your stock symbol
alphavantage_api_key = "8G8Y7ZRQCJ4EI849"  # Replace with your Alpha Vantage API key
eps_surprise_df = get_eps_surprise(symbol, alphavantage_api_key)
print(eps_surprise_df)
