# Will perform the cleaning of the user data.You will need clean the user data, 
# look out for NULL values, errors with dates, incorrectly typed values and rows filled with the wrong information.
import pandas as pd
import numpy as np
import yaml
import re

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
        email_regex = r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
        df.loc[~df['email_address'].str.match(email_regex),'email_address'] = np.nan 

        # Cleans alphabetical columns
        alpha_column = ['first_name','last_name','company','country','country_code']
        for column in alpha_column:
            df[column] = df[column].apply(self.keep_alpha)

        # Clean country code
        df = df[df['country_code'].isin(['GB', 'DE', 'US'])]
        df = df.reset_index(drop=True)
        df = df.dropna()
        return df
    
    # Method to only keep alphabetical values
    def keep_alpha(self,val):
        return ''.join(filter(str.isalpha, str(val)))
    
    # Cleans card data's table's 'expiary_date','date_payment_confirmed' columns to datetime
    def clean_card_data(self,df):
        df = df.dropna()
        df = df.drop_duplicates()
        # Date columns cleaned
        df['expiry_date'] = pd.to_datetime(df['expiry_date'],format='%m/%y',errors='coerce')
        df['date_payment_confirmed'] = df['date_payment_confirmed'].str.strip()
        df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'],format='%Y-%m-%d',errors='coerce')
        # df['card_provider'] = 
        return df

    # Read bank account number regex for each bank 
    def read_bank_regex():
        with open('bank_regex.yaml','r') as file:
            bank_regex = yaml.safe_load(file)
        return bank_regex
    
    # Checks if value is float
    def is_float(val):
        try:
            float_value = float(val)
            return True
        except ValueError:
            return False

    # Clean store data, filter, drop columns, parse datetime, clean text, convert numeric, retain countries."
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
    
    # converts all weights to "...kg"pattern
    def convert_product_weights(self, val):
        multi_pack_pattern_kg = r"\d+ x \d"
        multi_pack_pattern_g = r"\d+ x \d+g"
        if val.endswith('kg'):
            kilograms = float(val[:-2])
        elif val.endswith('g'):
            if re.match(multi_pack_pattern_g, val):  # Check if it matches the multi-pack pattern
                parts = val.split(' x ')
                weight_per_unit = int(parts[0])
                quantity = int(parts[1].replace('g', ''))
                total_weight_g = weight_per_unit * quantity
                kilograms = total_weight_g / 1000
            else:
                grams = float(val[:-1])
                kilograms = grams / 1000
        elif val.endswith('ml'):
            liters =  float(val[:-2]) / 1000
            kilograms = liters
        
        elif re.match(multi_pack_pattern_kg, val):  # Check if it matches the multi-pack pattern
            parts = val.split(' x ')
            weight_per_unit = int(parts[0])
            quantity = int(parts[1])
            total_weight_g = weight_per_unit * quantity
            kilograms = total_weight_g / 1000
        elif val.endswith('m'):
            liters = float(val[:-1])
            kilograms = liters 
        elif val.endswith('oz'):
            grams = float(val[:-2])
            kilograms = grams / 1000
        else:
            return val
    
        return float(kilograms)
    
    def clean_product_data(self,df):
        removed_status = ['Still_avaliable', 'Removed'] 
        ok_categories = ['toys-and-games', 'sports-and-leisure','pets', 'homeware','health-and-beauty','food-and-drink', 'diy']
        df['removed'] = df['removed'].where(df['removed'].isin(removed_status), other=pd.NA)
        df['weight'] = df['weight'].astype(str).apply(self.convert_product_weights)
        df['date_added'] = pd.to_datetime(df['date_added'],format='%Y-%m-%d',errors='coerce')
        # astype(str) method to convert the entire 'product_price' column to strings, ensuring that all values are treated as strings regardless of their original data types.
        df['product_price'] = df['product_price'].astype(str)
        # Replace values that don't start with '£' with NaN
        df.loc[~df['product_price'].str.startswith('£'), 'product_price'] = pd.NA
        df['category'] = df['category'].where(df['category'].isin(ok_categories), other=pd.NA)

        df = df.dropna()
        df = df.drop_duplicates()
    
        return df
    
    def clean_orders_data(self,df):
        df = df.drop(['first_name'], axis=1)
        df = df.drop(['last_name'], axis=1)
        df = df.drop(['1'], axis=1)

        df = df.dropna()
        df = df.drop_duplicates()
        return df
    
    def clean_date_details(self,df):
        date_columns = ['year', 'month', 'day']
        for column in date_columns:
            df[column] = pd.to_numeric(df[column],errors='coerce')
        # Convert 'timestamp' column to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S', errors='coerce')  

        df.dropna(subset=['timestamp'], inplace=True)
        # Combine columns into a single datetime column
        df['accurate_date'] = pd.to_datetime(df[['year', 'month', 'day']]) + df['timestamp'].apply(lambda x: pd.Timedelta(hours=x.hour, minutes=x.minute, seconds=x.second))
        return df
    

    # Function to alter data types in the tables of SQL database
    def set_datatype(self, engine, table, df):
        with engine.connect() as conn:
            # Iterate over each row in the DataFrame
            for i, row in df.iterrows():
                # ALTER TABLE query for each row
                # if row['store_details_table'] == table.column
                query = f"ALTER TABLE {table} ALTER COLUMN {row['store_details_table']} TYPE {row['required_date_type']} USING {row['store_details_table']}::{row['required_date_type']} WHERE COLUMN = row['required_data_type'];"
                q_exec = conn.execute(query)
        
        return "query successful"


        return data, columns


        # # only acceptable providers
        # df = df[df['card_provider'].isin([])]
        # card number regex
        # Clean phone number

        ###help needed!
        """ 

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
        