# import os
# import yfinance as yf
# import pandas as pd

# class StockDataDownloader:
#     def __init__(self, tickers, start_dates, end_dates, folder_path):
#         self.tickers = tickers
#         self.start_dates = start_dates
#         self.end_dates = end_dates
#         self.folder_path = folder_path
    
#     def download_stock_data(self):
#         for i, ticker in enumerate(self.tickers):
#             try:
#                 # Fetch the stock data
#                 stock_data = yf.download(ticker, start=self.start_dates[i], end=self.end_dates[i])
                
#                 # Create the StockData folder if it doesn't exist
#                 os.makedirs(self.folder_path, exist_ok=True)
                
#                 # Create a folder for the current stock if it doesn't exist
#                 stock_folder_path = os.path.join(self.folder_path, ticker)
#                 os.makedirs(stock_folder_path, exist_ok=True)
                
#                 # Create a folder for the current date range if it doesn't exist
#                 date_folder = f"{self.start_dates[i]}_to_{self.end_dates[i]}"
#                 date_folder_path = os.path.join(stock_folder_path, date_folder)
#                 os.makedirs(date_folder_path, exist_ok=True)
                
#                 # Save the data to a CSV file in the date folder
#                 file_name = f"{ticker}_stock_data.csv"
#                 file_path = os.path.join(date_folder_path, file_name)
#                 stock_data.to_csv(file_path)
                
#                 print(f"Stock data for {ticker} downloaded and saved to {file_path}")
#             except Exception as e:
#                 print(f"Error downloading stock data for {ticker}: {str(e)}")

# # Define the ticker symbols, date ranges, and folder path
# tickers = ["SAN", "PEO.F", "INGA.AS"]
# start_dates = ["2023-01-01", "2023-01-01", "2023-02-01"]
# end_dates = ["2023-06-01", "2023-03-01", "2023-06-01"]
# folder_path = "StockData"  # Specify the desired parent folder path here

# # Create an instance of the StockDataDownloader class
# downloader = StockDataDownloader(tickers, start_dates, end_dates, folder_path)

# # Download and save the stock data
# downloader.download_stock_data()
