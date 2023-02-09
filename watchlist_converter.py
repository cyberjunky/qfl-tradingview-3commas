#!/usr/bin/env python3
"""Cyberjunky's crypto helpers."""
import argparse
import csv
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="TradingView Watchlist input file in .txt format",
                        type=str, required=True)
    parser.add_argument("--output", help="Alertzmanager.io output file in .csv format",
                        type=str, required=True)
    args = parser.parse_args()

    # open the input trading view file
    with open(args.input, "r") as f:
        tradingview_watchlist = f.read()

    tradingview_watchlist = tradingview_watchlist.split(",")
    logging.info(f"There are {len(set(tradingview_watchlist))} symbols in the watchlist")

    # open the output alertzmanager file
    with open(args.output, "w") as outfile:
        fields = ['symbol', 'instrument', 'quote_asset']
        writer = csv.DictWriter(outfile, fieldnames=fields, delimiter=',', lineterminator = '\n')
        writer.writeheader()

        for item in tradingview_watchlist:
            instrument = item.split(":")[1]
            if instrument.endswith("BTC"):
                quote_asset = "BTC"
                coin = instrument.replace("BTC", "").strip()
            if instrument.endswith("USDT"):
                quote_asset = "USDT"
                coin = instrument.replace("USDT", "").strip()

            writer.writerow({'symbol': item.strip(), 'instrument': coin.strip(), 'quote_asset': quote_asset})

    logging.info(f"Saved watchlist for alertzmanager.io as {args.output}.")
    outfile.close()