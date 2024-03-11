# from database_utils import DatabaseConnector
# from data_extraction import DataExtractor
from data_cleaning import DataCleaning
import pandas as pd
# from pandasgui import show
def main():
    """ #initialize DatabaseConnector
    db_connector = DatabaseConnector()

    #read database credentials from YAML file and initialize database engine
    cred_data = db_connector.read_db_creds()
    engine = db_connector.init_db_engine(cred_data)
    print(engine)
    
    #initialize DataExtractor 
    extractor = DataExtractor(engine)

    #get the names of all tables in the database
    tables = db_connector.list_db_tables(engine)

    #loop through each table and extract data into a DataFrame
    for table_name in tables:
       df = extractor.read_rds_table(table_name)
       df.to_csv(table_name+'.csv') """
    
    #

    data_cleaner = DataCleaning()
    df = pd.read_csv('legacy_users.csv')
    df = data_cleaner.clean_user_data(df)
    df = df.set_index('index')
    df.to_csv('legacy_users.csv')
   
    """ df = pd.read_csv('legacy_users.csv')
    print(df['country'].value_counts()) """

if __name__ == "__main__":
    main()
