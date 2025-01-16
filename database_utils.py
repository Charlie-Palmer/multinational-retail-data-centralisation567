from sqlalchemy import create_engine, inspect
import pandas as pd
import yaml

class DatabaseConnector:
    #Reads database credentials from a yaml file   
    def read_db_creds(self):
        with open('db_creds.yaml', 'r') as f:
            credentials_dict = yaml.safe_load(f)
        return credentials_dict

    #Initialises an SQLAlchemy engine using the credentials given
    def init_db_engine(self):
        credentials = self.read_db_creds()
        rds_engine = create_engine(
            f"postgresql://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@"
            f"{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}"
        )
        return rds_engine

    #Retrieves a list of table names in the database
    def list_db_tables(self):
        rds_engine = self.init_db_engine()
        inspector = inspect(rds_engine)
        tables = inspector.get_table_names()
        
        return tables
    #Reads credentials for local database
    def read_my_creds(self):
        with open('my_creds.yaml', 'r') as my_creds:
            credentials_dict = yaml.safe_load(my_creds)
        return credentials_dict
    
    #Connect to PostgreSQL database using psycopg2    
    def connect_to_pg(self, database):
        credentials = self.read_my_creds()
        engine = create_engine(
            f"postgresql://{credentials['PG_USER']}:{credentials['PG_PASSWORD']}@"
            f"{credentials['PG_HOST']}:{credentials['PG_PORT']}/{database}"
        )
        return engine

    #Uploads dataframe to a specified table in the local database
    def upload_to_db(self, df: pd.DataFrame, table_name: str):        
        pgadmin_engine = self.connect_to_pg("sales_data")
        df.to_sql(table_name, con=pgadmin_engine, if_exists='replace', index=False)
        print(f"Data uploaded to {table_name}.")

            