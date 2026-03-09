import yfinance as yf
import pandas as pd
import requests
from io import StringIO

# Load S&P 500 ticker list from Wikipedia
sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(sp500_url, headers=headers, timeout=10)
response.raise_for_status()

html = StringIO(response.text)
ticker_df = pd.read_html(html)[0]
tickers = ticker_df["Symbol"].dropna().tolist()
tickers = [ticker.replace(".", "-") for ticker in tickers]

MIN_PRICE = 2
MAX_PRICE = 300
MIN_VOLUME = 500_000
MIN_GAP = -5
MIN_REL_VOLUME = 0.8

print(f"Downloading data for {len(tickers)} tickers...")

data = yf.download(
    tickers=tickers,
    period="10d",
    group_by="ticker",
    auto_adjust=False,
    progress=True,
    threads=True
)

results = []

for ticker in tickers:
    try:
        if ticker not in data:
            continue

        ticker_data = data[ticker].dropna()

        if ticker_data.empty or len(ticker_data) < 6:
            continue

        prev_close = ticker_data["Close"].iloc[-2]
        today_open = ticker_data["Open"].iloc[-1]
        price = ticker_data["Close"].iloc[-1]
        volume = ticker_data["Volume"].iloc[-1]

        avg_volume = ticker_data["Volume"].iloc[-6:-1].mean()
        rel_volume = volume / avg_volume if avg_volume > 0 else 0

        gap_percent = ((today_open - prev_close) / prev_close) * 100

        if (
            MIN_PRICE <= price <= MAX_PRICE
            and volume >= MIN_VOLUME
            and gap_percent >= MIN_GAP
            and rel_volume >= MIN_REL_VOLUME
        ):
            results.append({
                "Ticker": ticker,
                "Price": round(float(price), 2),
                "Gap %": round(float(gap_percent), 2),
                "Volume": int(volume),
                "Avg Volume": int(avg_volume),
                "Rel Volume": round(float(rel_volume), 2)
            })

    except Exception as e:
        print(f"Error with {ticker}: {e}")

if results:
    df = pd.DataFrame(results)
    df = df.sort_values(
        ["Rel Volume", "Gap %", "Volume"],
        ascending=False
    )

    top = df.head(10)

    print("\nTop Momentum Candidates\n")
    print(top.to_string(index=False))

    df.to_csv("scanner_results.csv", index=False)
    top["Ticker"].to_csv("watchlist.csv", index=False)

    print("\nSaved full results -> scanner_results.csv")
    print("Saved watchlist -> watchlist.csv")
else:
    print("\nNo stocks matched the current filter.")
