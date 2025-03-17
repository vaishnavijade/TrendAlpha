
# 💹 Alpha Strategy: Trend Detection & Trade Execution  

A quantitative trading strategy designed to optimize **alpha (excess returns over a benchmark)** using historical price data. This system employs a **dual moving average (SMA) crossover approach** to generate buy/sell signals, balancing risk and reward with **Sharpe Ratio optimization**.  

This strategy won **First Prize** at the **IIT Bombay Hackathon**, sponsored by **Dhan**, for its effective trade execution and risk-adjusted performance. 🎉  

## 🌟 Key Features  
- **📈 Dual Moving Average Crossover:**  
  - Uses **10-period (fast)** and **50-period (slow)** SMAs to detect trends and generate trade signals.  
- **⚠️ Risk Management:**  
  - Implements **2% stop-loss** and **4% take-profit** rules to protect capital.  
- **📊 Sharpe Ratio Calculation:**  
  - Evaluates the risk-adjusted performance of the strategy.  
- **🛠️ Backtesting Engine:**  
  - Simulates historical performance on **OHLCV** market data.  
- **🌐 Flexible & Scalable:**  
  - Can be applied to any asset class following the same data format.  

## 📥 Input Data  
- **Historical OHLCV Data (Open, High, Low, Close, Volume)**  
- Dataset includes **30 financial instruments** (2019-2022) in CSV format.  

## 📋 Strategy Logic  
### **Indicators Used**  
- **Fast SMA:** 10-period simple moving average.  
- **Slow SMA:** 50-period simple moving average.  

### **Trade Execution Rules**  
- **Buy Signal:** When the **fast SMA crosses above** the slow SMA.  
- **Sell Signal:** When the **fast SMA crosses below** the slow SMA.  

### **Risk Management**  
- **Stop-Loss:** Caps downside risk at **2% per trade**.  
- **Take-Profit:** Locks in gains at **4% per trade**.  

## 📊 Performance Evaluation  
### **Sharpe Ratio Formula**  
```python
Sharpe Ratio = (Annualized Return - Risk-Free Rate) / Annualized Volatility
