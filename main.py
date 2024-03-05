from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Initialise database connector
connector = DatabaseConnector()

# Read database credentials from YAML file and initialize database engine
creds = connector.read_db_creds("db_creds.yaml")
engine = connector.init_db_engine(creds)

# Initialize DataExtractor with the database engine
extractor = DataExtractor(engine)

# Extract data from the required table (assuming 'dim_users' is the table name)
dim_users_df = extractor.read_rds_table(connector, 'dim_users')

# Initialize DataCleaning
cleaner = DataCleaning()

# Clean the extracted data
cleaned_dim_users_df = cleaner.clean_user_data(dim_users_df)

# Upload the cleaned data to the 'dim_users' table in the 'sales_data' database
connector.upload_to_db(cleaned_dim_users_df, 'dim_users')