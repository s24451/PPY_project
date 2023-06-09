import os
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class DataDownloader:
    def __init__(self, companies, start_date, end_date):
        self.companies = companies

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

                if not data.empty:
                    # Save the downloaded data to a CSV file in the specific folder
                    formatted_start_date = self.start_date.strftime("%Y-%m-%d")
                    formatted_end_date = self.end_date.strftime("%Y-%m-%d")

                    filename = os.path.join(directory, f"{folder_company_name}_data_{formatted_start_date}_to_{formatted_end_date}.csv")
                    data.to_csv(filename)
                    print(f"Downloaded data for {company} and saved as {filename}")
                else:
                    print(f"No data available for {company}")
            except Exception as e:
                print(f"Failed to download data for {company}: {str(e)}")

        print("Data downloading complete.")
