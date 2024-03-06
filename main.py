from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from pandasgui import show

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

    # Step 2: Create an empty dictionary to store table data
    table_data = {}

    # Step 3: Loop through each table and extract data into a DataFrame
    for table_name in tables:
        table_data[table_name] = extractor.read_rds_table(db_connector, table_name)

    # Step 4: Display all tables using PandasGUI
    show(table_data)

if __name__ == "__main__":
    main()
