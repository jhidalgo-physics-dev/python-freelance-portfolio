import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Ask user for ticker
ticker = input("Enter stock ticker: ").upper()

# Download data
data = yf.download(ticker, start="2022-01-01", end="2024-01-01")

# Moving averages
data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

# Save statistics
summary = data.describe()
summary.to_csv(f"{ticker}_summary.csv")

# Plot
plt.figure(figsize=(10,6))
plt.plot(data["Close"], label="Close Price")
plt.plot(data["MA20"], label="20 Day MA")
plt.plot(data["MA50"], label="50 Day MA")

plt.title(f"{ticker} Price Analysis")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()

# Save chart
plt.savefig(f"{ticker}_analysis.png")

plt.show()