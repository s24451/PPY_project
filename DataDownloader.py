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


# Converting the dates to datetime.date if they are not already
        if isinstance(start_date, str):
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            self.start_date = start_date

        if isinstance(end_date, str):
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            self.end_date = end_date


#dictionary to map name to the ticker symbol 
    def download_data(self):
        ticker_mapping = {
            "Microsoft": "MSFT",
            "Apple": "AAPL",
            "Google": "GOOGL",
            "Amazon": "AMZN"
        }


#for all companies in the list of companies 
        for company in self.companies:
            folder_company_name = company.replace(" ", "_")
            directory = os.path.join(os.getcwd(), folder_company_name)

  # Defining the directory name where the data will be stored
            if not os.path.exists(directory):
                os.makedirs(directory)

            if company in ticker_mapping:
                ticker = ticker_mapping[company]
            else:
                print(f"Invalid stock company: {company}")
                continue

            try:
                # Adjusting the end date to include the next day
                end_date_adjusted = (self.end_date + timedelta(days=1)).strftime("%Y-%m-%d")
            
                data = yf.download(ticker, start=self.start_date, end=end_date_adjusted)
                 # Reseting the index so that 'Date' is a column
                data = data.reset_index()

                if not data.empty:
                    # Saving the downloaded data to a CSV file in the specific folder
                    filename = self.generate_file_path(company, self.start_date, self.end_date)
                    data.to_csv(filename)
                    data = self.convert_data_types(data)
                    data = self.clean_data(data)
                    self.data[company] = data
                    print(f"Downloaded data for {company} and saved as {filename}")
                else:
                    print(f"No data available for {company}")
            except Exception as e:
                print(f"Failed to download data for {company}: {str(e)}")

    def convert_data_types(self, data):
         # Converting 'Date' column to datetime type if it exists
        if 'Date' in data.columns:
            try:
                data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
            except ValueError:
                pass
    # Converting numerical columns to float type
        numerical_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']
        try:
            data[numerical_columns] = data[numerical_columns].astype(float)
        except ValueError:
            pass

        try:
            data['Volume'] = data['Volume'].astype(int)
        except ValueError:
            pass

        return data

    def clean_data(self, data):
        #handling missing or incorrect values
        cleaned_data = data.copy()

        if 'Date' in cleaned_data.columns:
            cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'], errors='coerce')

        numerical_columns = cleaned_data.select_dtypes(include=[np.number]).columns.tolist()
        cleaned_data[numerical_columns] = cleaned_data[numerical_columns].apply(pd.to_numeric, errors='coerce')
        cleaned_data[numerical_columns] = cleaned_data[numerical_columns].fillna(cleaned_data[numerical_columns].mean())

        return cleaned_data

    def cleanup_data(self):
         # Deleting the downloaded data files after the program is finished
        for company in self.companies:
            filename = self.generate_file_path(company, self.start_date, self.end_date)
            if os.path.exists(filename):
                os.remove(filename)

    def generate_file_path(self, company, start_date, end_date):
        folder_company_name = company.replace(" ", "_")
        formatted_start_date = start_date.strftime("%Y-%m-%d")
        formatted_end_date = end_date.strftime("%Y-%m-%d")
        return os.path.join(
            os.getcwd(),
            folder_company_name,
            f"{folder_company_name}_data_{formatted_start_date}_to_{formatted_end_date}.csv"
        )
    
