from data_extraction import DataExtractor
from database_utils import DatabaseConnector
#from data_upload import DataLoader
# from data_extraction import DataExtractor
#from data_cleaning import DataCleaning

import pandas as pd
def main():
    link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
    db_connector = DatabaseConnector()
    cred_data = db_connector.read_db_creds()
    engine = db_connector.init_db_engine(cred_data)
    pdf_extractor = DataExtractor(engine)
    df = pdf_extractor.retrieve_pdf_data(link)
    print(df)

    """ # Uploading to postgres database 
    
    df = pd.read_csv('clean_legacy_users.csv')
    db_connector = DatabaseConnector()
    cred_data = db_connector.read_local_creds()
    local_engine = db_connector.local_db_engine(cred_data)

    data_loader = DataLoader(local_engine)
    data_loader.upload_to_db(df,'clean_legacy_user') """



    """ # Initialize DatabaseConnector
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
    

    """ # Cleaning data
    data_cleaner = DataCleaning()
    df = pd.read_csv('legacy_users.csv')
    df = data_cleaner.clean_user_data(df)
    df = df.reset_index(drop=True)
    df.drop(df.columns[0:2], axis=1, inplace=True)
    df.to_csv('clean_legacy_users.csv')
      """
   
    """ 
    df = pd.read_csv('legacy_users.csv')
    print(df['country'].value_counts())
    """

if __name__ == "__main__":
    main()
