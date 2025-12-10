"""Reformat the existing dailyData_export.csv into Yahoo-style CSVs for importing."""

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

EXPORT_FILE = Path("dailyData_export.csv")
OUTPUT_DIR = Path("import_csvs")


def load_export():
    grouped = defaultdict(list)
    with EXPORT_FILE.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            grouped[row["symbol"]].append(row)
    return grouped


def format_rows(rows):
    formatted = []
    for row in rows:
        date = datetime.strptime(row["date"], "%m/%d/%y").strftime("%Y-%m-%d")
        price = float(row["price"])
        volume = int(float(row["volume"]))
        formatted.append((date, price, volume))
    formatted.sort(key=lambda item: item[0])
    return formatted


def write_import_file(symbol, rows):
    filename = OUTPUT_DIR / f"{symbol}_yahoo.csv"
    with filename.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])
        for date, price, volume in rows:
            writer.writerow([date, f"{price:.2f}", f"{price:.2f}", f"{price:.2f}", f"{price:.2f}", f"{price:.2f}", volume])


def main():
    if not EXPORT_FILE.exists():
        raise SystemExit(f"{EXPORT_FILE} not found. Run sqlite export first.")
    OUTPUT_DIR.mkdir(exist_ok=True)
    grouped = load_export()
    for symbol, rows in grouped.items():
        clean = format_rows(rows)
        write_import_file(symbol, clean)
    print(f"Created {len(grouped)} Yahoo-style CSVs under {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
