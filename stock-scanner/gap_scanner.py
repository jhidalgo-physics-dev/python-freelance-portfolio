import yfinance as yf
import pandas as pd

# Load tickers from CSV
ticker_df = pd.read_csv("tickers.csv")
tickers = ticker_df["Ticker"].dropna().tolist()

results = []

MIN_PRICE = 2
MAX_PRICE = 300
MIN_VOLUME = 500_000
MIN_GAP = -5
MIN_REL_VOLUME = 0.8

for ticker in tickers:
    try:
        data = yf.Ticker(ticker).history(period="10d", auto_adjust=False)

        if data.empty or len(data) < 6:
            print(f"Skipping {ticker}: not enough data")
            continue

        prev_close = data["Close"].iloc[-2]
        today_open = data["Open"].iloc[-1]
        price = data["Close"].iloc[-1]
        volume = data["Volume"].iloc[-1]

        avg_volume = data["Volume"].iloc[-6:-1].mean()
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
                "Price": round(price, 2),
                "Gap %": round(gap_percent, 2),
                "Volume": int(volume),
                "Avg Volume": int(avg_volume),
                "Rel Volume": round(rel_volume, 2)
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