from database_utils import DatabaseConnector

# Initialise database connector
connector = DatabaseConnector()

# Read database credentials from YAML file and initialize database engine
creds = connector.read_db_creds("db_creds.yaml")
engine = connector.init_db_engine(creds)

