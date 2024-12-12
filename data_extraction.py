from database_utils import DatabaseConnector
import boto3
import pandas as pd
import requests
import tabula

class DataExtractor:
    
    def __init__(self):
        pass
        
    #reads data from a specified table in the RDS database and returns a dataframe
    def read_rds_table(self, db_connector: DatabaseConnector, table_name: str):
        query = f"SELECT * FROM {table_name}"
        with db_connector.init_db_engine().connect() as connection:
            data = pd.read_sql(query, connection)
        return data
    
    #Reads data from a specific PDF and returns it as a dataframe
    def retrieve_pdf_data():
        file = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        card_details_list = tabula.read_pdf(file, lattice=True, pages = 'all')
        card_details = pd.concat(card_details_list,ignore_index=True)
        return card_details
    #Key used to access store data
    def api_key(self):
        return {"x-api-key" : "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
    
    #Creates a list of store numbers    
    def list_store_numbers(self):
        number_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        response = requests.get(number_endpoint, headers=self.api_key)
        return response.json()['number_stores']

    #Takes the list of store numbers to get the data for each store and collate it into a dataframe
    def retrieve_store_data(self):
        number_of_stores = self.list_store_numbers()
        store_data_list = []       
        for store_number in range (0, number_of_stores):
                store_endpoint = f"https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}"
                response = requests.get(store_endpoint, headers=self.api_key)
                store_data_list.append(response.json())

        return pd.DataFrame(store_data_list)

    #Extracts product data from S3 and returns it as a dataframe
    def extract_from_s3(self):
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket = 'data-handling-public', Key = 'products.csv')
        return pd.read_csv(response['Body'])

    #Retrieves event data from a json file and returns it as a dataframe
    def retrieve_events_data(self):
        url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
        response = requests.get(url)
        return pd.DataFrame(response.json())

