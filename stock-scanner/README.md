# Momentum Scanner

A Python-based stock scanning tool designed to identify momentum candidates using gap percentage, trading volume, and relative volume.

This project was built as a practical trading workflow tool and a demonstration of Python-based financial data analysis.

---

## Features

* Scan S&P 500 or a custom momentum universe
* Sort candidates by:

  * Relative Volume
  * Gap Percentage
  * Volume
* Configurable filter presets (testing or trading)
* Relative volume calculation
* Automatic CSV export of results
* Timestamped scan history
* Clean terminal summary output
* Packaged executable version

---

## Example Output

The scanner identifies candidates meeting momentum conditions and displays the top results.

Example summary:

```
Scan Summary
------------
Universe: momentum
Sort mode: gap
Filter preset: trade
Tickers scanned: 29
Candidates found: 2
Tickers skipped: 1
```

---

## Output Files

Scan results are automatically saved to the `results` folder.

Example:

```
results/
scan_momentum_gap_trade_2026-03-10_1245.csv
watchlist_momentum_gap_trade_2026-03-10_1245.csv
```

These files can be used for watchlists or further analysis.

---

## Executable Version

A standalone Windows executable can be generated using PyInstaller.

```
py -m PyInstaller --onefile --name MomentumScanner gap_scanner.py
```

The resulting executable can be found in the `dist` folder.

Example application structure:

```
MomentumScanner-App
├── MomentumScanner.exe
├── momentum_universe.csv
└── results
```

---

## Technologies Used

* Python
* Pandas
* yfinance
* requests
* PyInstaller

---

## Future Improvements

Planned enhancements include:

* real-time momentum radar monitoring
* customizable filter parameters
* graphical dashboard interface
* alert notifications for new signals
