import numpy as np

class StatisticsCalculator:
    def calculate_statistics(self, data_list, column='Close'):
        statistics = {} #empty dictionary to store calculations

        for data in data_list:
            company = data['Company'][0]#extracting company name
            if data.empty:
                statistics[company] = [0, 'N/A', 'N/A']
            else:
                values = data[column]
                mean = round(values.mean(),2)
                median = round(np.median(values), 2) if len(values) > 0 else 'N/A'
                std = round(values.std(),2) if len(values) > 1 else 'N/A'
                statistics[company] = [mean, median, std]#store for current company

        return statistics

