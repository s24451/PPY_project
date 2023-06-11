import numpy as np

class StatisticsCalculator:
    def calculate_statistics(self, data_list, column='Close'):
        statistics = {}

        for data in data_list:
            company = data['Company'][0]
            if data.empty:
                statistics[company] = [0, 'N/A', 'N/A']
            else:
                values = data[column]
                mean = round(values.mean(),2)
                median = round(np.median(values), 2) if len(values) > 0 else 'N/A'
                std = round(values.std(),2) if len(values) > 1 else 'N/A'
                statistics[company] = [mean, median, std]

        return statistics

