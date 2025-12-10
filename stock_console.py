# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ").strip()
        while option not in ["1", "2", "3", "4", "5", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ").strip()
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")


# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ").strip()
        while option not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ").strip()
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")
            input("Press Enter to continue...")


# Add new stock to track
def add_stock(stock_list):
    clear_screen()
    print("Add Stock ---")
    symbol = input("Enter Symbol: ").strip().upper()
    if not symbol:
        print("Symbol cannot be blank.")
        input("Press Enter to continue...")
        return
    existing = next((stock for stock in stock_list if stock.symbol.upper() == symbol), None)
    if existing:
        print(f"Stock {symbol} already exists.")
        input("Press Enter to continue...")
        return
    name = input("Enter Name: ").strip()
    shares_input = input("Enter Shares on Hand: ").strip()
    try:
        shares = float(shares_input)
    except ValueError:
        print("Invalid shares value.")
        input("Press Enter to continue...")
        return
    new_stock = Stock(symbol, name, shares)
    stock_list.append(new_stock)
    sortStocks(stock_list)
    print(f"{symbol} added to portfolio.")
    input("Press Enter to continue...")


# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ").strip()
        while option not in ["1", "2", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            option = input("Enter Menu Option: ").strip()
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        else:
            print("Returning to Manage Stocks Menu")
            input("Press Enter to continue...")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    if not stock_list:
        print("No stocks to buy shares for.")
        input("Press Enter to continue...")
        return
    symbol = input("Enter Symbol: ").strip().upper()
    stock = next((stk for stk in stock_list if stk.symbol.upper() == symbol), None)
    if not stock:
        print(f"{symbol} is not in the portfolio.")
        input("Press Enter to continue...")
        return
    shares_input = input("Enter Shares to Buy: ").strip()
    try:
        shares = float(shares_input)
    except ValueError:
        print("Invalid share amount.")
        input("Press Enter to continue...")
        return
    if shares <= 0:
        print("Enter a positive share amount.")
        input("Press Enter to continue...")
        return
    stock.buy(shares)
    print(f"{shares} shares added to {symbol}. New total: {stock.shares}")
    input("Press Enter to continue...")


# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    if not stock_list:
        print("No stocks to sell shares for.")
        input("Press Enter to continue...")
        return
    symbol = input("Enter Symbol: ").strip().upper()
    stock = next((stk for stk in stock_list if stk.symbol.upper() == symbol), None)
    if not stock:
        print(f"{symbol} is not in the portfolio.")
        input("Press Enter to continue...")
        return
    shares_input = input("Enter Shares to Sell: ").strip()
    try:
        shares = float(shares_input)
    except ValueError:
        print("Invalid share amount.")
        input("Press Enter to continue...")
        return
    if shares <= 0 or shares > stock.shares:
        print("Enter a positive share amount not greater than current holdings.")
        input("Press Enter to continue...")
        return
    stock.sell(shares)
    print(f"{shares} shares sold from {symbol}. New total: {stock.shares}")
    input("Press Enter to continue...")


# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    if not stock_list:
        print("No stocks in the portfolio.")
        input("Press Enter to continue...")
        return
    symbol = input("Enter Symbol to Remove: ").strip().upper()
    for idx, stock in enumerate(stock_list):
        if stock.symbol.upper() == symbol:
            del stock_list[idx]
            print(f"{symbol} removed from portfolio.")
            input("Press Enter to continue...")
            return
    print(f"{symbol} not found.")
    input("Press Enter to continue...")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Current Stocks ---")
    if not stock_list:
        print("No stocks being tracked.")
    else:
        sortStocks(stock_list)
        for stock in stock_list:
            print(f"{stock.symbol}: {stock.name} - {stock.shares} shares ({len(stock.DataList)} data points)")
    input("Press Enter to continue...")


# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    if not stock_list:
        print("No stocks available. Add a stock first.")
        input("Press Enter to continue...")
        return
    symbol = input("Enter Symbol to Add Data For: ").strip().upper()
    stock = next((stk for stk in stock_list if stk.symbol.upper() == symbol), None)
    if not stock:
        print(f"{symbol} is not tracked.")
        input("Press Enter to continue...")
        return
    date_input = input("Date (m/d/yy): ").strip()
    price_input = input("Closing Price: ").strip()
    volume_input = input("Volume: ").strip()
    try:
        date_value = datetime.strptime(date_input, "%m/%d/%y")
        price = float(price_input)
        volume = float(volume_input)
    except ValueError:
        print("Invalid data entered.")
        input("Press Enter to continue...")
        return
    stock.add_data(DailyData(date_value, price, volume))
    sortDailyData(stock_list)
    print("Daily data added.")
    input("Press Enter to continue...")


# Display Report for All Stocks
def display_report(stock_list):
    clear_screen()
    print("Stock Report ---")
    if not stock_list:
        print("No stocks to report.")
    else:
        sortDailyData(stock_list)
        for stock in stock_list:
            print(f"{stock.symbol} ({stock.name}) - {stock.shares} shares")
            if not stock.DataList:
                print("    No historical data.")
                continue
            closes = [data.close for data in stock.DataList]
            volumes = [data.volume for data in stock.DataList]
            latest = stock.DataList[-1]
            print(f"    Records: {len(stock.DataList)}  Latest: {latest.date.strftime('%m/%d/%y')} {latest.close:.2f}")
            print(f"    Close Range: {min(closes):.2f} - {max(closes):.2f}  Avg Close: {sum(closes)/len(closes):.2f}")
            print(f"    Total Volume: {sum(volumes):,.0f}")
            profit_loss = stock.profit_loss()
            percent = stock.profit_loss_percent()
            print(f"    Profit/Loss: ${profit_loss:,.2f} ({percent:+.2f}%)")
    input("Press Enter to continue...")


# Display Chart
def display_chart(stock_list):
    if not stock_list:
        print("No stocks to chart.")
        input("Press Enter to continue...")
        return
    clear_screen()
    print("Available Stocks:")
    sortStocks(stock_list)
    for stock in stock_list:
        print(f"{stock.symbol} - {stock.name}")
    symbol = input("Enter Symbol to Chart: ").strip()
    if not symbol:
        print("No symbol entered.")
        input("Press Enter to continue...")
        return
    display_stock_chart(stock_list, symbol)


# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data")
        print("2 - Load Data")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ").strip()
        while option not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Save Data")
            print("2 - Load Data")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ").strip()
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data saved.")
            input("Press Enter to continue...")
        elif option == "2":
            stock_list.clear()
            stock_data.load_stock_data(stock_list)
            sortStocks(stock_list)
            print("Data loaded.")
            input("Press Enter to continue...")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        else:
            print("Returning to Main Menu")
            input("Press Enter to continue...")


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieve Data From Web ---")
    if not stock_list:
        print("No stocks in portfolio.")
        input("Press Enter to continue...")
        return
    date_start = input("Enter Starting Date (m/d/yy): ").strip()
    date_end = input("Enter Ending Date (m/d/yy): ").strip()
    try:
        records = stock_data.retrieve_stock_web(date_start, date_end, stock_list)
        sortDailyData(stock_list)
        print(f"Retrieved {records} records.")
    except RuntimeWarning as err:
        print(err)
    except Exception:
        print("Unable to retrieve data. Check Chrome Driver path.")
    input("Press Enter to continue...")


# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import From CSV ---")
    if not stock_list:
        print("No stocks to import data for.")
        input("Press Enter to continue...")
        return
    symbol = input("Enter Symbol to Import For: ").strip().upper()
    filename = input("Enter Full Path to CSV File: ").strip()
    if not filename:
        print("Filename is required.")
        input("Press Enter to continue...")
        return
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        sortDailyData(stock_list)
        print(f"CSV data imported for {symbol}.")
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as err:
        print(f"Unable to import data: {err}")
    input("Press Enter to continue...")


# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)


# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()
