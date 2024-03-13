# This class will work as a utility class, in it you will be creating methods that help extract data from different data sources.
# The methods contained will be fit to extract data from a particular data source, these sources will include CSV files, an API and an S3 bucket.
import pandas as pd
import tabula as tb

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
    
   # Method to extract the database table to a pandas DataFrame.
    def read_rds_table(self, table_name):
        # Get the names of all tables in the database
        # tables = self.list_db_tables(table_name)
        # if table_name not in tables:
        #     raise ValueError(f"Table '{table_name}' not found in the database.")
        # Extract the table containing user data and return a pandas DataFrame.
        # ext_data, columns = tables
        df = pd.read_sql_table(table_name,self.engine)
        return df
    
    # Takes pdf in a link as an argument and returns a pandas DataFrame.
    def retrieve_pdf_data(self,file_link):
        list_data = tb.read_pdf(file_link,pages="all")
        df = pd.DataFrame(list_data)
        return df