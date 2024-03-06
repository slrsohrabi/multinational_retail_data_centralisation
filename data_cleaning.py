# Will perform the cleaning of the user data.You will need clean the user data, 
# look out for NULL values, errors with dates, incorrectly typed values and rows filled with the wrong information.
import pandas as pd

class DataCleaning:
    def __init__(self):
        pass
    
    #  This method will take in a Pandas DataFrame and table name to upload to as an argument.
    def clean_user_data(self,df):
        df = df.dropna()
        date_columns = ['birthday','another_date']
        for column in date_columns:
            df[column] = pd.to_datetime(df[column],errors='coerce')
        return df
