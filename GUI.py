import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from DataDownloader import DataDownloader
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import sys


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.create_main_window()
        self.create_layout()
        self.data_list = []  # Store the processed data
        self.data_downloader = None
        self.window.protocol("WM_DELETE_WINDOW", self.handle_window_close)
        self.volume_analysis_button_pressed = False

    def create_main_window(self):
        self.window.title("Stock Data Analysis")
        self.window.geometry("1000x1000")
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
        self.process_button.grid(row=5, column=0, padx=10, pady=20)

        self.volume_analysis_button = tk.Button(self.window, text="Perform Volume Analysis",
                                                command=self.handle_volume_analysis_button, bg="light blue")
        self.volume_analysis_button.grid(row=5, column=1, padx=10)

        self.result_label = tk.Label(self.window, text="", bg="white")
        self.result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.plot_frame = tk.Frame(self.window, bg="white")
        self.plot_frame.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky="n")

    def create_bank_selection(self):
        self.bank_var1 = tk.BooleanVar()
        self.bank_var2 = tk.BooleanVar()

        self.bank_label = tk.Label(self.window, text="Select Company(s):", bg="white", font=("Helvetica", 10))
        self.bank_label.grid(row=0, column=0, padx=10, pady=10)

        self.bank_check1 = ttk.Checkbutton(self.window, text="Microsoft", variable=self.bank_var1)
        self.bank_check1.grid(row=1, column=0, padx=10)

        self.bank_check2 = ttk.Checkbutton(self.window, text="Apple", variable=self.bank_var2)
        self.bank_check2.grid(row=1, column=1, padx=10)

    def handle_process_button(self):
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")

        banks = []
        self.start_date = start_date
        self.end_date = end_date

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

        self.data_list = []  # Clear the existing data

        for bank in banks:
            filename = os.path.join(os.getcwd(), bank.replace(" ", "_"),
                                    f"{bank.replace(' ', '_')}_data_{start_date}_to_{end_date}.csv")
            data = pd.read_csv(filename)
            cleaned_data = downloader.clean_data(data)
            cleaned_data['Company'] = bank  # Add a column for the company name
            self.data_list.append(cleaned_data)

        self.update_graph()

        results = []
        for data in self.data_list:
            average_closing_price = self.calculate_average_closing_price(data)
            results.append(f"Company: {data['Company'][0]}, Average Closing Price: {average_closing_price:.2f}")

        self.result_label.config(
            text=f"Selected dates: {start_date} - {end_date}\n" + "\n".join(results)
        )



    def handle_volume_analysis_button(self):
        if not self.data_list:
            self.result_label.config(text="No data available for volume analysis.")
            return

        # Clear the existing graph
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.window, bg="white")
        self.plot_frame.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky="n")

        volume_fig, volume_ax = plt.subplots(figsize=(6, 4), dpi=100)

        for data in self.data_list:
            volume_ax.plot(data['Date'], data['Volume'], label=data['Company'][0])

        volume_ax.set_xlabel('Date')
        volume_ax.set_ylabel('Volume')
        volume_ax.set_title('Stock Volume Variation')
        volume_ax.legend()

        # Adjust x-axis margins and spacing
        volume_fig.autofmt_xdate()
        volume_fig.tight_layout(pad=2.0, h_pad=1.0)

        volume_canvas = FigureCanvasTkAgg(volume_fig, master=self.plot_frame)
        volume_canvas.draw()
        volume_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Set the flag to indicate volume analysis button is pressed
        self.volume_analysis_button_pressed = True

        # Update the result label
        results = []
        for data in self.data_list:
            average_closing_price = self.calculate_average_closing_price(data)
            average_volume = self.calculate_average_volume(data)
            results.append(f"Company: {data['Company'][0]}, Average Closing Price: {average_closing_price:.2f}, Average Volume: {average_volume:.2f}")

        self.result_label.config(
            text=f"Selected dates: {self.start_date} - {self.end_date}\n" + "\n".join(results)
        )

    def calculate_average_closing_price(self, data):
        if not data.empty:
            return data['Close'].mean()
        return 0

    def calculate_average_volume(self, data):
        if not data.empty:
            return data['Volume'].mean()
        return 0

    def handle_window_close(self):
        if self.data_downloader:
            self.data_downloader.cleanup_data()
        sys.exit()

    def update_graph(self):
        # Clear the plot frame
        self.plot_frame.destroy()
        self.plot_frame = tk.Frame(self.window, bg="white")
        self.plot_frame.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky="n")

        self.plot_data()

    def plot_data(self):
        if not self.data_list:
            return

        figure, ax = plt.subplots(figsize=(6, 4), dpi=100)

        for data in self.data_list:
            ax.plot(data['Date'], data['Close'], label=data['Company'][0])

        ax.set_xlabel('Date')
        ax.set_ylabel('Closing Price')
        ax.set_title('Stock Price Variation')
        ax.legend()

        # Adjust x-axis margins and spacing
        figure.autofmt_xdate()
        figure.tight_layout(pad=2.0, h_pad=1.0)

        canvas = FigureCanvasTkAgg(figure, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def run(self):
        self.window.mainloop()


# Create an instance of the GUI class
gui = GUI()
gui.run()
