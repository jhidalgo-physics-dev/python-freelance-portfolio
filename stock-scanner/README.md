# Momentum Stock Scanner

A Python tool that scans stocks for momentum characteristics such as price gaps, volume spikes, and relative volume.

## Features

- Loads ticker universe from CSV
- Calculates daily gap percentage
- Filters by price range
- Filters by minimum volume
- Calculates relative volume
- Ranks strongest candidates
- Exports results to CSV

## Output Files

scanner_results.csv  
Full dataset of stocks that passed filters.

watchlist.csv  
Top candidates ranked by momentum metrics.

## Requirements

Python packages:

- pandas
- yfinance

Install with:

pip install pandas yfinance

## How to Run

From the project folder:

py gap_scanner.py

## Configuration

Filters can be adjusted inside the script:

MIN_PRICE  
MAX_PRICE  
MIN_VOLUME  
MIN_GAP  
MIN_REL_VOLUME