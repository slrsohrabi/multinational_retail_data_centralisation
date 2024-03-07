# This class will work as a utility class, in it you will be creating methods that help extract data from different data sources.
# The methods contained will be fit to extract data from a particular data source, these sources will include CSV files, an API and an S3 bucket.
import pandas as pd

####Should I create another engine, there is already one in the database_utils.py in a method?
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
    def read_rds_table(self,db_connector,table_name):
        # Get the name of the table containing user data
        tables = db_connector.list_db_tables(self.engine)
        if table_name not in tables:
            raise ValueError(f"Table '{table_name}' not found in the database.")
        # Extract the table containing user data and return a pandas DataFrame.
        ext_data, columns = self.list_db_tables(table_name)
        df = pd.DataFrame(ext_data,columns = columns)
        return df

import pandas as pd

class DataExtractor:
    def __init__(self, engine):
        self.engine = engine

    # Method to list the columns of a given table in the RDS database.
    def list_db_tables(self, table_name):
        with self.engine.connect() as conn:
            query = f"SELECT * FROM {table_name}"
            result = conn.execute(query)
            data = result.fetchall()
            # columns = result.keys()
        return data
    
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

