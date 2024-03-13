class DataLoader:
    def __init__(self,engine):
        self.engine = engine
    
    # This method will take in a Pandas DataFrame and table name to upload to as an argument.
    def upload_to_db(self,df,table_name):
        with self.engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)

   