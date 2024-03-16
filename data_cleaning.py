# Will perform the cleaning of the user data.You will need clean the user data, 
# look out for NULL values, errors with dates, incorrectly typed values and rows filled with the wrong information.
import pandas as pd
import numpy as np
import yaml

class DataCleaning:
    def __init__(self):
        pass
    
    #  This method will take in a Pandas DataFrame and table name to upload to as an argument.
    def clean_user_data(self,df):
        df = df.dropna()
        df = df.drop_duplicates()
        
        # Cleans date_columns
        date_columns = ['date_of_birth','join_date']
        # for column in date_columns:
        #     df[column] = pd.to_datetime(df[column],format= '%Y-%m-%d',errors='coerce')
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'],format= '%Y-%m-%d',errors='coerce')
        df['join_date'] = pd.to_datetime(df['join_date'],format= '%Y-%m-%d',errors='coerce')
        # clean email using email regex from regexlib.com
        email_regex = '^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
        df.loc[~df['email_address'].str.match(email_regex),'email_address'] = np.nan 

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

    def clean_card_data(self,df):
        df = df.dropna()
        df = df.drop_duplicates()
        # Date columns cleaned
        df['expiry_date'] = pd.to_datetime(df['expiry_date'],format='%m/%y',errors='coerce')
        df['date_payment_confirmed'] = df['date_payment_confirmed'].str.strip()
        df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'],format='%Y-%m-%d',errors='coerce')
        # df['card_provider'] = 
        return df
    
    def read_bank_regex():
        with open('bank_regex.yaml','r') as file:
            bank_regex = yaml.safe_load(file)
        return bank_regex
    
    def clean_store_data(self,df):
        # Clean by store type
        store_types = ['Local','Super Store','Mall Kiosk','Outlet','Web Portal']
        str_columns = ['address','locality','store_code','store_type','country_code']
        df['store_type'] = df['store_type'].where(df['store_type'].isin(store_types), other=pd.NA)
        # Drops obsolete columns
        df = df.drop(['lat'], axis=1)  # Specify axis=1 to drop columns
        # Clean datetime column
        df['opening_date'] = pd.to_datetime(df['opening_date'],format='%Y-%m-%d',errors='coerce')
        # clean alphabetical columns using the keep_alpha() function
        df['locality'] = df['locality'].apply(self.keep_alpha)
        for col in str_columns:
            df[col] = df[col].astype(str)
        # only keep numeric in the columns
        df['staff_numbers'] = pd.to_numeric(df['staff_numbers'], errors='coerce')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df = df[df['country_code'].isin(['GB', 'DE', 'US'])]
        df = df.dropna()
        df = df.drop_duplicates()
        return df 


        # # only acceptable providers
        # df = df[df['card_provider'].isin([])]
        # card number regex
        # Clean phone number

        ###help!
        """ 
        df['phone_number'] = df['phone_number'].replace({r'\+44': '0', r'\(': '', r'\)': '', r'-': '', r' ': '',r'\^44': '0',r'(?<=\d)x(?=\d)': '#'}, regex=True)

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
        