import pandas as pd

#Methods to clean data from each of the data sources.
class DataCleaning:
    def __init__(self):
        pass
    
    #  This method will take in a Pandas DataFrame and table name to upload to as an argument.
    def clean_user_data(self,df,table_name):
        df.dropna()
        date_columns = ['birthday','another_date']
        for column in date_columns:
            df[column] = pd.to_datetime(df[column],errors='coerce')
        return df
