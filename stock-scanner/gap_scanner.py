import yfinance as yf
import pandas as pd
import requests
import sys
import os
from io import StringIO
from datetime import datetime

os.makedirs("results", exist_ok=True)

# Choose scanner mode: "sp500" or "momentum"
scan_mode = input("Choose scan mode ('sp500' or 'momentum'): ").strip().lower()
sort_mode = input("Choose sort mode ('rel_volume', 'gap', or 'volume'): ").strip().lower()
limit_input = input("How many top results should be shown? (default 10): ").strip()

if limit_input == "":
    result_limit = 10
else:
    result_limit = int(limit_input)

if scan_mode not in ["sp500", "momentum"]:
    raise ValueError("scan_mode must be 'sp500' or 'momentum'")

if sort_mode not in ["rel_volume", "gap", "volume"]:
    raise ValueError("sort_mode must be 'rel_volume', 'gap', or 'volume'")

if scan_mode == "sp500":
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(sp500_url, headers=headers, timeout=10)
    response.raise_for_status()

    html = StringIO(response.text)
    ticker_df = pd.read_html(html)[0]
    tickers = ticker_df["Symbol"].dropna().tolist()
    tickers = [ticker.replace(".", "-") for ticker in tickers]

elif scan_mode == "momentum":
    ticker_df = pd.read_csv("momentum_universe.csv")
    tickers = ticker_df["Ticker"].dropna().tolist()

else:
    raise ValueError("scan_mode must be 'sp500' or 'momentum'")

filter_mode = input("Choose filter mode ('test' or 'trade'): ").strip().lower()

if filter_mode == "test":
    MIN_PRICE = 2
    MAX_PRICE = 150
    MIN_VOLUME = 300_000
    MIN_GAP = -2
    MIN_REL_VOLUME = 0.8

elif filter_mode == "trade":
    MIN_PRICE = 2
    MAX_PRICE = 20
    MIN_VOLUME = 500_000
    MIN_GAP = 0
    MIN_REL_VOLUME = 1.2

else:
    raise ValueError("filter_mode must be 'test' or 'trade'")

print(f"Running scanner in {scan_mode} mode on {len(tickers)} tickers...")
print(f"Using {filter_mode} filters")

print(f"Downloading data for {len(tickers)} tickers...")

data = yf.download(
    tickers=tickers,
    period="10d",
    group_by="ticker",
    auto_adjust=False,
    progress=False,
    threads=True
)

results = []
skipped_tickers = []

for ticker in tickers:
    try:
        if ticker not in data.columns.get_level_values(0):
            skipped_tickers.append(ticker)
            continue
        
        ticker_data = data[ticker]

        if ticker_data is None or ticker_data.empty:
            skipped_tickers.append(ticker)
            continue

        ticker_data = ticker_data.dropna()

        if ticker_data.empty or len(ticker_data) < 6:
            skipped_tickers.append(ticker)
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

    except Exception:
        skipped_tickers.append(ticker)

if results:
    df = pd.DataFrame(results)
    if sort_mode == "rel_volume":
        df = df.sort_values(["Rel Volume", "Gap %", "Volume"], ascending=False)
    elif sort_mode == "gap":
        df = df.sort_values(["Gap %", "Rel Volume", "Volume"], ascending=False)
    elif sort_mode == "volume":
        df = df.sort_values(["Volume", "Rel Volume", "Gap %"], ascending=False)
    else:
        raise ValueError("sort_mode must be 'rel_volume', 'gap', or 'volume'")

    top = df.head(result_limit)

    print(f"\nTop {result_limit} Momentum Candidates (sorted by {sort_mode})\n")
    print(top.to_string(index=False))

    # create timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # create dynamic filenames
    results_filename = f"scan_{scan_mode}_{sort_mode}_{filter_mode}_{timestamp}.csv"
    watchlist_filename = f"watchlist_{scan_mode}_{sort_mode}_{filter_mode}_{timestamp}.csv"

    # Save files
    df.to_csv(f"results/{results_filename}", index=False)
    top["Ticker"].to_csv(f"results/{watchlist_filename}", index=False)

    print(f"\nSaved full results to: {results_filename}")
    print(f"Saved watchlist to: {watchlist_filename}")
else:
    print("\nNo stocks matched the current filter.")

tickers_scanned = len(tickers)
candidates_found = len(results)
tickers_skipped = len(skipped_tickers)

print("\nScan Summary")
print("------------")
print(f"Universe: {scan_mode}")
print(f"Sort mode: {sort_mode}")
print(f"Filter preset: {filter_mode}")
print(f"Tickers scanned: {tickers_scanned}")
print(f"Candidates found: {candidates_found}")
print(f"Tickers skipped: {tickers_skipped}")

if getattr(sys, 'frozen', False):
    input("\nScan complete. Press Enter to exit...")