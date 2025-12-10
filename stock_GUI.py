# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import stock_data
from stock_class import Stock, DailyData
from utilities import display_stock_chart, sortStocks, sortDailyData


class StockApp:
    def __init__(self):
        self.stock_list = []
        if path.exists("stocks.db") == False:
            stock_data.create_database()

        self.root = Tk()
        self.root.title("(myname) Stock Manager")
        self.root.geometry("1100x680")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Load Data", command=self.load)
        filemenu.add_command(label="Save Data", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV From Yahoo! Finance...", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)

        chartmenu = Menu(self.menubar, tearoff=0)
        chartmenu.add_command(label="Show Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=chartmenu)

        self.root.config(menu=self.menubar)

        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.grid(sticky="nsew")
        main_frame.columnconfigure(0, weight=1, minsize=320)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        left_frame = Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)

        portfolio_label = Label(left_frame, text="Portfolio", font=("Helvetica", 12, "bold"))
        portfolio_label.pack(anchor="w")

        listbox_frame = Frame(left_frame)
        listbox_frame.pack(fill=BOTH, expand=True)
        self.stockList = Listbox(listbox_frame, exportselection=False, activestyle="dotbox")
        self.stockList.pack(side=LEFT, fill=BOTH, expand=True)
        stock_scrollbar = Scrollbar(listbox_frame, orient=VERTICAL, command=self.stockList.yview)
        stock_scrollbar.pack(side=RIGHT, fill=Y)
        self.stockList.configure(yscrollcommand=stock_scrollbar.set)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        delete_button = Button(left_frame, text="Delete Stock", command=self.delete_stock)
        delete_button.pack(fill=X, pady=(5, 0))

        add_frame = LabelFrame(left_frame, text="Add Stock")
        add_frame.pack(fill=X, pady=6)
        Label(add_frame, text="Symbol").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.addSymbolEntry = Entry(add_frame)
        self.addSymbolEntry.grid(row=0, column=1, padx=2, pady=2)
        Label(add_frame, text="Name").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.addNameEntry = Entry(add_frame)
        self.addNameEntry.grid(row=1, column=1, padx=2, pady=2)
        Label(add_frame, text="Shares").grid(row=2, column=0, sticky="w", padx=2, pady=2)
        self.addSharesEntry = Entry(add_frame)
        self.addSharesEntry.grid(row=2, column=1, padx=2, pady=2)
        add_button = Button(add_frame, text="Add Stock", command=self.add_stock)
        add_button.grid(row=3, column=0, columnspan=2, pady=(4, 2), sticky="ew")

        shares_frame = LabelFrame(left_frame, text="Update Shares")
        shares_frame.pack(fill=X, pady=6)
        Label(shares_frame, text="Shares").grid(row=0, column=0, padx=2, pady=4, sticky="w")
        self.updateSharesEntry = Entry(shares_frame, width=12)
        self.updateSharesEntry.grid(row=0, column=1, padx=2, pady=4)
        buy_button = Button(shares_frame, text="Buy", command=self.buy_shares)
        buy_button.grid(row=0, column=2, padx=2, pady=4)
        sell_button = Button(shares_frame, text="Sell", command=self.sell_shares)
        sell_button.grid(row=0, column=3, padx=2, pady=4)

        data_frame = LabelFrame(left_frame, text="Add Daily Data")
        data_frame.pack(fill=X, pady=6)
        Label(data_frame, text="Date (m/d/yy)").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.dailyDateEntry = Entry(data_frame, width=12)
        self.dailyDateEntry.grid(row=0, column=1, padx=2, pady=2)
        Label(data_frame, text="Close").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.dailyPriceEntry = Entry(data_frame, width=12)
        self.dailyPriceEntry.grid(row=1, column=1, padx=2, pady=2)
        Label(data_frame, text="Volume").grid(row=2, column=0, sticky="w", padx=2, pady=2)
        self.dailyVolumeEntry = Entry(data_frame, width=12)
        self.dailyVolumeEntry.grid(row=2, column=1, padx=2, pady=2)
        daily_button = Button(data_frame, text="Save Daily Data", command=self.add_daily_data)
        daily_button.grid(row=3, column=0, columnspan=2, pady=(4, 2), sticky="ew")

        right_frame = Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", pady=5)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        self.headingLabel = Label(right_frame, text="Select a stock to view history", font=("Helvetica", 12, "bold"))
        self.headingLabel.grid(row=0, column=0, sticky="w")

        notebook = ttk.Notebook(right_frame)
        notebook.grid(row=1, column=0, sticky="nsew", pady=(5, 0))

        history_frame = Frame(notebook)
        report_frame = Frame(notebook)
        notebook.add(history_frame, text="History")
        notebook.add(report_frame, text="Report")

        self.dailyDataList = Text(history_frame, wrap=NONE)
        history_scroll = Scrollbar(history_frame, orient=VERTICAL, command=self.dailyDataList.yview)
        self.dailyDataList.configure(yscrollcommand=history_scroll.set)
        self.dailyDataList.pack(side=LEFT, fill=BOTH, expand=True)
        history_scroll.pack(side=RIGHT, fill=Y)

        self.stockReport = Text(report_frame, wrap=WORD)
        report_scroll = Scrollbar(report_frame, orient=VERTICAL, command=self.stockReport.yview)
        self.stockReport.configure(yscrollcommand=report_scroll.set)
        self.stockReport.pack(side=LEFT, fill=BOTH, expand=True)
        report_scroll.pack(side=RIGHT, fill=Y)

        self.root.mainloop()

    def refresh_stock_list(self):
        self.stockList.delete(0, END)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)

    def load(self):
        self.stockList.delete(0, END)
        stock_data.load_stock_data(self.stock_list)
        self.refresh_stock_list()
        if self.stock_list:
            self.stockList.selection_set(0)
        messagebox.showinfo("Load Data", "Data Loaded")
        self.display_stock_data()

    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    def add_stock(self):
        symbol = self.addSymbolEntry.get().strip().upper()
        name = self.addNameEntry.get().strip()
        shares_input = self.addSharesEntry.get().strip()
        if not symbol or not name or not shares_input:
            messagebox.showwarning("Add Stock", "Enter symbol, name, and shares.")
            return
        try:
            shares = float(shares_input)
        except ValueError:
            messagebox.showerror("Add Stock", "Shares must be a number.")
            return
        if any(stock.symbol.upper() == symbol for stock in self.stock_list):
            messagebox.showwarning("Add Stock", f"{symbol} already exists.")
            return
        new_stock = Stock(symbol, name, shares)
        self.stock_list.append(new_stock)
        self.refresh_stock_list()
        index = next((idx for idx, stock in enumerate(self.stock_list) if stock.symbol == symbol), 0)
        self.stockList.selection_clear(0, END)
        self.stockList.selection_set(index)
        self.stockList.see(index)
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)
        self.display_stock_data()
        messagebox.showinfo("Add Stock", f"{symbol} added to portfolio.")

    def buy_shares(self):
        stock = self._get_selected_stock()
        if not stock:
            messagebox.showwarning("Buy Shares", "Select a stock first.")
            return
        shares_input = self.updateSharesEntry.get().strip()
        try:
            shares = float(shares_input)
        except ValueError:
            messagebox.showerror("Buy Shares", "Enter a numeric share amount.")
            return
        if shares <= 0:
            messagebox.showwarning("Buy Shares", "Share amount must be positive.")
            return
        stock.buy(shares)
        self.updateSharesEntry.delete(0, END)
        self.display_stock_data()
        messagebox.showinfo("Buy Shares", "Shares Purchased")

    def sell_shares(self):
        stock = self._get_selected_stock()
        if not stock:
            messagebox.showwarning("Sell Shares", "Select a stock first.")
            return
        shares_input = self.updateSharesEntry.get().strip()
        try:
            shares = float(shares_input)
        except ValueError:
            messagebox.showerror("Sell Shares", "Enter a numeric share amount.")
            return
        if shares <= 0 or shares > stock.shares:
            messagebox.showwarning("Sell Shares", "Amount must be positive and no more than current shares.")
            return
        stock.sell(shares)
        self.updateSharesEntry.delete(0, END)
        self.display_stock_data()
        messagebox.showinfo("Sell Shares", "Shares Sold")

    def delete_stock(self):
        stock = self._get_selected_stock()
        if not stock:
            messagebox.showwarning("Delete Stock", "Select a stock to remove.")
            return
        self.stock_list.remove(stock)
        self.refresh_stock_list()
        self.display_stock_data()
        messagebox.showinfo("Delete Stock", f"{stock.symbol} removed from portfolio.")

    def add_daily_data(self):
        stock = self._get_selected_stock()
        if not stock:
            messagebox.showwarning("Add Daily Data", "Select a stock first.")
            return
        date_input = self.dailyDateEntry.get().strip()
        price_input = self.dailyPriceEntry.get().strip()
        volume_input = self.dailyVolumeEntry.get().strip()
        try:
            date_value = datetime.strptime(date_input, "%m/%d/%y")
            price_value = float(price_input)
            volume_value = float(volume_input)
        except ValueError:
            messagebox.showerror("Add Daily Data", "Check date, price, and volume formats.")
            return
        stock.add_data(DailyData(date_value, price_value, volume_value))
        sortDailyData(self.stock_list)
        self.dailyDateEntry.delete(0, END)
        self.dailyPriceEntry.delete(0, END)
        self.dailyVolumeEntry.delete(0, END)
        self.display_stock_data()
        messagebox.showinfo("Add Daily Data", "Data Saved")

    def refresh_daily_display(self):
        self.dailyDataList.config(state=NORMAL)
        self.dailyDataList.delete("1.0", END)
        self.stockReport.config(state=NORMAL)
        self.stockReport.delete("1.0", END)

    def display_stock_data(self):
        self.refresh_daily_display()
        selection = self.stockList.curselection()
        if not selection:
            self.headingLabel['text'] = "Select a stock to view history"
            self.dailyDataList.config(state=DISABLED)
            self.stockReport.config(state=DISABLED)
            return
        symbol = self.stockList.get(selection[0])
        stock = next((stk for stk in self.stock_list if stk.symbol == symbol), None)
        if not stock:
            self.headingLabel['text'] = "Select a stock to view history"
            self.dailyDataList.config(state=DISABLED)
            self.stockReport.config(state=DISABLED)
            return
        sortDailyData([stock])
        self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        if not stock.DataList:
            self.dailyDataList.insert(END, "No history available.\n")
            self.stockReport.insert(END, "No historical data has been recorded for this stock.")
            self.dailyDataList.config(state=DISABLED)
            self.stockReport.config(state=DISABLED)
            return
        self.dailyDataList.insert(END, "- Date -      - Price -    - Volume -\n")
        self.dailyDataList.insert(END, "----------------------------------------\n")
        for daily_data in stock.DataList:
            row = f"{daily_data.date.strftime('%m/%d/%y')}   {'${:,.2f}'.format(daily_data.close)}   {int(daily_data.volume):,}\n"
            self.dailyDataList.insert(END, row)
        closes = [data.close for data in stock.DataList]
        volumes = [data.volume for data in stock.DataList]
        latest = stock.DataList[-1]
        self.stockReport.insert(END, f"Records: {len(stock.DataList)}\n")
        self.stockReport.insert(END, f"Latest: {latest.date.strftime('%m/%d/%y')} @ ${latest.close:,.2f}\n")
        self.stockReport.insert(END, f"Close Range: ${min(closes):,.2f} - ${max(closes):,.2f}\n")
        self.stockReport.insert(END, f"Avg Close: ${sum(closes)/len(closes):,.2f}\n")
        self.stockReport.insert(END, f"Total Volume: {int(sum(volumes)):,}\n")
        profit_loss = stock.profit_loss()
        percent = stock.profit_loss_percent()
        self.stockReport.insert(END, f"Profit/Loss: ${profit_loss:,.2f} ({percent:+.2f}%)\n")
        self.dailyDataList.config(state=DISABLED)
        self.stockReport.config(state=DISABLED)

    def update_data(self, evt):
        self.display_stock_data()

    def display_chart(self):
        stock = self._get_selected_stock()
        if not stock:
            messagebox.showwarning("Display Chart", "Select a stock before showing a chart.")
            return
        display_stock_chart(self.stock_list, stock.symbol)

    def scrape_web_data(self):
        if not self.stock_list:
            messagebox.showwarning("Get Data From Web", "Add at least one stock before retrieving data.")
            return
        dateFrom = simpledialog.askstring("Starting Date", "Enter Starting Date (m/d/yy)")
        if not dateFrom:
            return
        dateTo = simpledialog.askstring("Ending Date", "Enter Ending Date (m/d/yy)")
        if not dateTo:
            return
        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
            sortDailyData(self.stock_list)
            self.display_stock_data()
            messagebox.showinfo("Get Data From Web", "Data Retrieved")
        except RuntimeWarning:
            messagebox.showerror("Cannot Get Data from Web", "Check Path for Chrome Driver")
        except Exception:
            messagebox.showerror("Cannot Get Data from Web", "Unable to reach Yahoo! Finance.")

    def importCSV_web_data(self):
        selection = self.stockList.curselection()
        if not selection:
            messagebox.showwarning("Import CSV", "Select a stock before importing.")
            return
        symbol = self.stockList.get(selection[0])
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import", filetypes=[('Yahoo Finance! CSV', '*.csv')])
        if not filename:
            return
        try:
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            sortDailyData(self.stock_list)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", symbol + " Import Complete")
        except FileNotFoundError:
            messagebox.showerror("Import CSV", "File not found.")
        except Exception as err:
            messagebox.showerror("Import CSV", str(err))

    def _get_selected_stock(self):
        selection = self.stockList.curselection()
        if not selection:
            return None
        symbol = self.stockList.get(selection[0])
        return next((stock for stock in self.stock_list if stock.symbol == symbol), None)


def main():
    app = StockApp()


if __name__ == "__main__":
    main()
