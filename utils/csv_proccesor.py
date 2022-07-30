import csv
import pandas as pd
from datetime import datetime

dateparse = lambda x: datetime.strptime(x, '%m/%d')

class CsvProccesor():

    def __init__(self, csv_file_path):
        self.file_path = csv_file_path
        self.transaction_info = {}

    def proccess_csv(self):
        self.df = pd.read_csv(self.file_path, parse_dates=['Date'], date_parser=dateparse,index_col='Id')
        self.df['month'] = self.df['Date'].dt.month_name()
        self.transaction_info['total_balance'] = "{:.2f}".format(self.df['Transaction'].sum())
        self.transaction_info['avarage_debit'] = "{:.2f}".format(self.df[self.df['Transaction'] < 0].mean(numeric_only=True).values[0])
        self.transaction_info['avarage_credit'] = "{:.2f}".format(self.df[self.df['Transaction'] > 0].mean(numeric_only=True).values[0])
        self.transaction_info['month_transactions'] = self.df.groupby(self.df['month'])['Transaction'].count()
    
    def save_transactions_to_db(self, dao, user_id, file_name):
        list_df = self.df.to_dict("index")
        save_data = {"doc_source": file_name}
        for key, value in list_df.items():
            save_data['Id'] = key
            for k, v in list_df[key].items():
                if k != 'Date':
                    save_data[k] = v
                else:
                    save_data[k] = v.strftime("%Y-%m-%d")
            dao.save_transaction(user_id, save_data)