# This class will work as a utility class, in it you will be creating methods that help extract data from different data sources.
# The methods contained will be fit to extract data from a particular data source, these sources will include CSV files, an API and an S3 bucket.
import pandas as pd
import tabula as tb
import requests
import boto3

class DataExtractor:
    def __init__(self,engine):
        self.engine = engine

    # Method to read the data from the RDS database.
    def list_db_tables(self,table_name):
        with self.engine.connect() as conn:
            # Insert query
            query = f"SELECT * FROM {table_name}"
            result = conn.execute(query)
            # Fetch all rows of the result set
            data = result.fetchall()
            # Get column names from the result object
            columns = result.keys()
        return data, columns
    
   # SQL,AWS dta extraction
    def read_rds_table(self, table_name):
        # Get the names of all tables in the database
        # tables = self.list_db_tables(table_name)
        # if table_name not in tables:
        #     raise ValueError(f"Table '{table_name}' not found in the database.")
        # Extract the table containing user data and return a pandas DataFrame.
        # ext_data, columns = tables
        df = pd.read_sql_table(table_name,self.engine)
        return df
    
    # pdf data Extraction
    def retrieve_pdf_data(self,file_link):
        # list_data = tb.read_pdf(file_link,pages="all")
        # Read the PDF and extract all tables from all pages
        tables = tb.read_pdf(file_link, pages='all', multiple_tables=True)
        # Concatenate all tables into a single DataFrame
        combined_df = pd.concat(tables, ignore_index=True)

        # df = pd.concat(list_data)
        return combined_df
    


    #  takes in a link as an argument and returns a pandas DataFrame.
    def list_number_of_stores(self,storenum_endp,header_dict):
        response = requests.get(storenum_endp, headers=header_dict)
        print(type(response))
        if response.status_code == 200:
            data = response.json()
            print(data)
            store_num = data
            return store_num
        else:
            print("Error:", response.status_code)
            return None 
    
    #  API data extraction
    def retrieve_stores_data(self,store_ret_end,header_dict):
        response = requests.get(store_ret_end, headers=header_dict)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error:", response.status_code)
            return None 
        
    # data extraction from CSV format in an S3 bucket on AWS
    def extract_from_s3(self,bucket_name,object_key):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        df = pd.read_csv(obj['Body'])
        return df

