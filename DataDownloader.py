import os
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np 
import atexit

class DataDownloader:
    def __init__(self, companies, start_date, end_date):
        self.companies = companies
        self.data = {}
        atexit.register(self.cleanup_data)

        # Convert the dates to datetime.date if they are not already
        if isinstance(start_date, str):
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            self.start_date = start_date

        if isinstance(end_date, str):
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            self.end_date = end_date

    def download_data(self):
        for company in self.companies:
        # Replace spaces in company names with underscores for folder naming
            folder_company_name = company.replace(" ", "_")

        # Define the directory name where the data will be stored
            directory = os.path.join(os.getcwd(), folder_company_name)

        # Create the directory if it does not exist
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Download data for each selected company from Yahoo Finance
            if company == "Microsoft":
                ticker = "MSFT"
            elif company == "Apple":
                ticker = "AAPL"
            else:
                print(f"Invalid stock company: {company}")
                continue

            try:
            # Adjust the end date to include the next day
                end_date_adjusted = (self.end_date + timedelta(days=1)).strftime("%Y-%m-%d")

                data = yf.download(ticker, start=self.start_date, end=end_date_adjusted)

            # Reset the index so that 'Date' is a column
                data = data.reset_index()

                if not data.empty:
                # Save the downloaded data to a CSV file in the specific folder
                    formatted_start_date = self.start_date.strftime("%Y-%m-%d")
                    formatted_end_date = self.end_date.strftime("%Y-%m-%d")

                    filename = os.path.join(directory, f"{folder_company_name}_data_{formatted_start_date}_to_{formatted_end_date}.csv")
                    data.to_csv(filename)
                    data = self.convert_data_types(data)
                    data = self.clean_data(data)
                    self.data[company] = data
                    print(f"Downloaded data for {company} and saved as {filename}")
                # data_plotter = DataPlotter()
                # data_plotter.plot_data(data)
                else:
                    print(f"No data available for {company}")
            except Exception as e:
                print(f"Failed to download data for {company}: {str(e)}")


    def convert_data_types(self, data):
    # Convert 'Date' column to datetime type if it exists
        if 'Date' in data.columns:
            try:
                data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
            except ValueError:
                pass

    # Convert numerical columns to float type
        numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']
        try:
            data[numerical_columns] = data[numerical_columns].astype(float)
        except ValueError:
            pass

    # Convert 'Volume' column to integer type
        try:
            data['Volume'] = data['Volume'].astype(int)
        except ValueError:
            pass

        return data

    def clean_data(self, data):
        cleaned_data = data.copy()

    # Convert 'Date' column to datetime type if it exists
        if 'Date' in cleaned_data.columns:
            cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'], errors='coerce')

    # Convert numerical columns to float type
        numerical_columns = cleaned_data.select_dtypes(include=[np.number]).columns.tolist()
        cleaned_data[numerical_columns] = cleaned_data[numerical_columns].apply(pd.to_numeric, errors='coerce')

    # Fill missing values in numerical columns with column means
        cleaned_data[numerical_columns] = cleaned_data[numerical_columns].fillna(cleaned_data[numerical_columns].mean())

    # Drop rows with missing values in numerical columns
        cleaned_data = cleaned_data.dropna(subset=numerical_columns)

        return cleaned_data

    

        
    def cleanup_data(self):
        # Delete the downloaded data files
        for company in self.companies:
            filename = os.path.join(os.getcwd(), company.replace(" ", "_"),
                                    f"{company.replace(' ', '_')}_data_{self.start_date}_to_{self.end_date}.csv")
            if os.path.exists(filename):
                os.remove(filename)





