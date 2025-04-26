import pandas as pd
import numpy as np
import os
import zipfile
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    df.dropna(inplace=True)
    return df

class DualMA_Strategy(Strategy):
    fast_ma = 10
    slow_ma = 50
    stop_loss_pct = 0.02
    take_profit_pct = 0.04

    def init(self):
        price = self.data.Close
        self.sma_fast = self.I(SMA, price, self.fast_ma)
        self.sma_slow = self.I(SMA, price, self.slow_ma)

    def next(self):
        price = self.data.Close[-1]
        if crossover(self.sma_fast, self.sma_slow):
            self.buy(sl=price * (1 - self.stop_loss_pct), tp=price * (1 + self.take_profit_pct))
        elif crossover(self.sma_slow, self.sma_fast):
            self.position.close()

def run_optimized_backtest(file_path):
    df = load_data(file_path)
    bt = Backtest(df, DualMA_Strategy, cash=100000, commission=0.001, exclusive_orders=True)

    stats = bt.optimize(
        fast_ma=range(5, 30, 5),
        slow_ma=range(20, 100, 10),
        stop_loss_pct=[0.01, 0.02, 0.03],
        take_profit_pct=[0.03, 0.05, 0.07],
        maximize='Sharpe Ratio',
        constraint=lambda p: p.fast_ma < p.slow_ma,
        max_tries=50
    )

    sharpe_ratio = stats['Sharpe Ratio']
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    if sharpe_ratio > 1:
        print(f"File: {file_name} | Sharpe Ratio: {sharpe_ratio:.2f}")

        trades = stats['_trades']
        trade_details = trades[['EntryBar', 'ExitBar', 'EntryPrice', 'ExitPrice', 'Size', 'PnL']].copy()
        trade_details['name'] = file_name
        trade_details['entry datetime'] = pd.to_datetime(df.index[trade_details['EntryBar']]).strftime('%d %b %y')
        trade_details['exit datetime'] = pd.to_datetime(df.index[trade_details['ExitBar']]).strftime('%d %b %y')
        trade_details['entry price'] = trade_details['EntryPrice']
        trade_details['exit price'] = trade_details['ExitPrice']
        trade_details['quantity'] = trade_details['Size']
        trade_details['profit/loss value'] = trade_details['PnL']

        return trade_details[['name', 'entry datetime', 'entry price', 'exit datetime', 'exit price', 'quantity', 'profit/loss value']]
    else:
        print(f"File: {file_name} | Sharpe Ratio: {sharpe_ratio:.2f} (Below 1) - Skipping")
        return None

def process_all_files_in_zip(zip_file_path, output_csv):
    extracted_folder = "extracted_files"
    os.makedirs(extracted_folder, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
    print("ZIP file extracted successfully.")

    all_results = pd.DataFrame()
    for root, _, files in os.walk(extracted_folder):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file}")
                try:
                    trade_results = run_optimized_backtest(file_path)
                    if trade_results is not None:
                        all_results = pd.concat([all_results, trade_results], ignore_index=True)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    if not all_results.empty:
        all_results.to_csv(output_csv, index=False)
        print(f"Optimized trade results saved to: {output_csv}")
    else:
        print("No files produced a Sharpe Ratio > 1. No results saved.")

if __name__ == "__main__":
    zip_file_path = "/content/drive-download-20241217T111005Z-001.zip"
    output_csv = "/content/optimized_trade_results.csv"
    process_all_files_in_zip(zip_file_path, output_csv)
    #https://drive.google.com/drive/folders/1AW0tLyCwxhyFaQ8VMwNjQydbi0SLe9yP//testiglik
