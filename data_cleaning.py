# Will perform the cleaning of the user data.You will need clean the user data, 
# look out for NULL values, errors with dates, incorrectly typed values and rows filled with the wrong information.
import pandas as pd
import numpy as np

class DataCleaning:
    def __init__(self):
        pass
    
    #  This method will take in a Pandas DataFrame and table name to upload to as an argument.
    def clean_user_data(self,df):
        df = df.dropna()
        df = df.drop_duplicates()
        #df = df.drop(columns="unnamed")

        # Cleans date_columns
        date_columns = ['date_of_birth','join_date']
        for column in date_columns:
            df[column] = pd.to_datetime(df[column],errors='coerce')
        
        # clean email
        
        
        # Clean phone number

        ###help!
        """ 
        df['phone_number'] = df['phone_number'].replace({r'\+44': '0', r'\(': '', r'\)': '', r'-': '', r' ': '',r'\^44': '0',r'(?<=\d)x(?=\d)': '#'}, regex=True)
        uk_regex_exp = '^\s*\(?((\+0?44)?\)?[ \-]?(\(0\))|0)((20[7,8]{1}\)?[ \-]?[1-9]{1}[0-9]{2}[ \-]?[0-9]{4})|([1-8]{1}[0-9]{3}\)?[ \-]?[1-9]{1}[0-9]{2}[ \-]?[0-9]{3}))\s*$'    
        us_regex_exp = '^(\(?\d\d\d\)?)?( |-|\.)?\d\d\d( |-|\.)?\d{4,4}(( |-|\.)?[ext\.]+ ?\d+)?$'
        de_regex_exp = '^((00|\+)49)?(0?[2-9][0-9]{1,})$'


        # Create masks for each country
        uk_mask = (df['country_code'] == 'GB') & (~df['phone_number'].str.match(uk_regex_exp))
        us_mask = (df['country_code'] == 'US') & (~df['phone_number'].str.match(us_regex_exp))
        de_mask = (df['country_code'] == 'DE') & (~df['phone_number'].str.match(de_regex_exp))

        # Replace phone numbers that don't match the regex patterns with NaN
        df.loc[uk_mask, 'phone_number'] = np.nan
        df.loc[us_mask, 'phone_number'] = np.nan
        df.loc[de_mask, 'phone_number'] = np.nan 
        """

        """ if df['country_code'] == 'GB' :
            df.loc[~df['phone_number'].str.match(uk_regex_exp), 'phone_number'] = np.nan # For every row  where the 'phone_number' column does not match the country expression, replace the value with NaN

        elif df['country_code'] == 'US' :
            df.loc[~df['phone_number'].str.match(us_regex_exp), 'phone_number'] = np.nan # For every row  where the 'phone_number' column does not match the country expression, replace the value with NaN

        elif df['country_code'] == 'DE' :
            df.loc[~df['phone_number'].str.match(de_regex_exp), 'phone_number'] = np.nan # For every row  where the 'phone_number' column does not match the country expression, replace the value with NaN
 """
        
        
        # Cleans alphabetical columns
        alpha_column = ['first_name','last_name','company','country','country_code']
        for column in alpha_column:
            df[column] = df[column].apply(self.keep_alpha)
        
        # Clean country code
        df = df[df['country_code'].isin(['GB', 'DE', 'US'])]

        df = df.reset_index(drop=True)

        return df
    # Method to only keep alphabetical values
    def keep_alpha(self,val):
        return ''.join(filter(str.isalpha, str(val)))
