import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class DataExtractor:
    def __init__(self):
        pass

    #the following function is to extract data from yfinance
    def get_data (self, symbol, start_date, end_date, interval):
        

        self.data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        self.data.columns = self.data.columns.droplevel(1)
        print("Data extraction complete.")
        return self.data
        

    #the following function is to plot the data
    def plot_data (self, data):
        
        data[['Close','Open','High','Low']].plot(title='EUR/USD Exchange Rate', figsize=(10, 6))
        plt.xlabel('Date')
        plt.ylabel('Exchange Rate')
        plt.show()

    #the following function is to save the data as csv
    def get_data_as_csv(self):
        
        user_input = input("do you want to save the data as csv? y/n: ")
        if user_input.lower() == 'y':
            return self.data.to_csv("data.csv")
        else:
            print("Data not saved as csv.")