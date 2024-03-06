from database_utils import DatabaseConnector
from data_extraction import DataExtractor

def main():
    # Initialize DatabaseConnector
    db_connector = DatabaseConnector()

    # Read database credentials from YAML file and initialize database engine
    cred_data = db_connector.read_db_creds()
    engine = db_connector.init_db_engine(cred_data)

    # Initialize DataExtractor with the database engine
    extractor = DataExtractor(engine)

    # Step 1: Get the names of all tables in the database
    tables = db_connector.list_db_tables(engine)

    # Step 2: Loop through each table and display its data
    for table_name in tables:
        print(f"Table: {table_name}")
        table_data_df = extractor.read_rds_table(db_connector, table_name)
        print(table_data_df)
        print("="*50)  # Separator between tables

if __name__ == "__main__":
    main()
