#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    stock_list.sort(key=lambda stock: stock.symbol.upper())


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda data: data.date)


# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    matching_stock = None
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            matching_stock = stock
            break
    if not matching_stock:
        print(f"No stock found for symbol {symbol}")
        return
    if not matching_stock.DataList:
        print(f"No historical data to chart for {symbol}")
        return
    sortDailyData([matching_stock])
    dates = [data.date for data in matching_stock.DataList]
    closes = [data.close for data in matching_stock.DataList]
    volumes = [data.volume for data in matching_stock.DataList]
    fig, ax_price = plt.subplots()
    ax_price.plot(dates, closes, marker="o", color="#1f77b4", label="Close Price")
    ax_price.set_xlabel("Date")
    ax_price.set_ylabel("Price", color="#1f77b4")
    ax_price.tick_params(axis="y", labelcolor="#1f77b4")
    ax_volume = ax_price.twinx()
    ax_volume.bar(dates, volumes, alpha=0.2, color="#7f7f7f", label="Volume")
    ax_volume.set_ylabel("Volume", color="#7f7f7f")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.suptitle(f"{matching_stock.symbol} - Closing Price & Volume", y=1.02)
    plt.show()
