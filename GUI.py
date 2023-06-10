import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from DataDownloader import DataDownloader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.create_main_window()
        self.create_layout()

    def create_main_window(self):
        self.window.title("Stock Data Analysis")
        self.window.geometry("400x400")
        self.window.config(bg="white")

    def create_layout(self):
        self.create_bank_selection()

        self.start_date_label = tk.Label(self.window, text="Start Date:", bg="white", font=("Helvetica", 10))
        self.start_date_label.grid(row=3, column=0, padx=10, pady=10)

        self.start_date_entry = DateEntry(self.window, background='light blue', foreground='black', borderwidth=2,
                                          font=("Helvetica", 10))
        self.start_date_entry.grid(row=3, column=1, padx=10)

        self.end_date_label = tk.Label(self.window, text="End Date:", bg="white", font=("Helvetica", 10))
        self.end_date_label.grid(row=4, column=0, padx=10, pady=10)

        self.end_date_entry = DateEntry(self.window, background='light blue', foreground='black', borderwidth=2,
                                        font=("Helvetica", 10))
        self.end_date_entry.grid(row=4, column=1, padx=10)

        self.process_button = tk.Button(self.window, text="Process Data", command=self.handle_process_button,
                                        bg="light blue")
        self.process_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

        self.result_label = tk.Label(self.window, text="", bg="white")
        self.result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.plot_frame = tk.Frame(self.window, bg="white")
        self.plot_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def create_bank_selection(self):
        self.bank_var1 = tk.BooleanVar()
        self.bank_var2 = tk.BooleanVar()

        self.bank_label = tk.Label(self.window, text="Select Bank(s):", bg="white", font=("Helvetica", 10))
        self.bank_label.grid(row=0, column=0, padx=10, pady=10)

        self.bank_check1 = ttk.Checkbutton(self.window, text="Microsoft", variable=self.bank_var1)
        self.bank_check1.grid(row=1, column=0, padx=10)

        self.bank_check2 = ttk.Checkbutton(self.window, text="Apple", variable=self.bank_var2)
        self.bank_check2.grid(row=1, column=1, padx=10)

    def handle_process_button(self):
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")

        banks = []

        if self.bank_var1.get():
            banks.append("Microsoft")
        if self.bank_var2.get():
            banks.append("Apple")

        print(f"Before processing: start date - {start_date}, end date - {end_date}, companies - {banks}")

        print(f"Companies: {banks}")

        if not start_date or not end_date or not banks:
            self.result_label.config(text="Please select both start and end dates, and at least one bank.")
            return
        downloader = DataDownloader(banks, start_date, end_date)
        downloader.download_data()
        data_list = []
        
        for bank in banks:
            filename = os.path.join(os.getcwd(), bank.replace(" ", "_"),
                                f"{bank.replace(' ', '_')}_data_{start_date}_to_{end_date}.csv")
            data = pd.read_csv(filename)
            cleaned_data = downloader.clean_data(data)
            cleaned_data['Company'] = bank  # Add a column for company name
            data_list.append(cleaned_data)

        self.plot_data(data_list)

        self.result_label.config(text=f"Selected dates: {start_date} - {end_date}, Bank(s): {', '.join(banks)}")


    def plot_data(self, data_list):
        figure, ax = plt.subplots(figsize=(6, 4), dpi=100)

        for data in data_list:
            ax.plot(data['Date'], data['Close'], label=data['Company'][0])

        ax.set_xlabel('Date')
        ax.set_ylabel('Closing Price')
        ax.set_title('Stock Price Variation')
        ax.legend()

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)



    def run(self):
        self.window.mainloop()


# Create an instance of the GUI class
gui = GUI()
gui.run()
