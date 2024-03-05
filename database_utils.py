#Will use to connect with and upload data to the database.
import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector:
    def __init__(self):
        pass

    #This will read the credentials yaml file and return a dictionary of the credentials.
    def read_db_creds(self):
        with open('db_creds.yaml','r') as file:
            cred_data = yaml.safe_load(file)
        return cred_data

    #Will read the credentials from the return of read_db_creds and initialise and return an sqlalchemy database engine.
    def init_db_engine(self,cred_data):
        # Construct database connection URL
        db_url = f"postgresql://{cred_data['RDS_USER']}:{cred_data['RDS_PASSWORD']}@{cred_data['RDS_HOST']}:{cred_data['RDS_PORT']}/{cred_data['RDS_DATABASE']}"
        # Create database engine
        engine = create_engine(db_url)
        return engine
    
    #Lists all the tables in the database so you know which tables you can extract data from.
    def list_db_tables(self,engine):
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return tables

    # This method will take in a Pandas DataFrame and table name to upload to as an argument.
    def upload_to_db(self,df,table_name):
        with self.engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)





