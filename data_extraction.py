import pandas as pd
from database_utils import DatabaseConnector
import tabula
import requests
import boto3


class DataExtractor:
    def __init__(self) -> None:
        self.api_details()
        
    #reads data from a specified table in the RDS database
    def read_rds_table(self, db_connector: DatabaseConnector, table_name: str):
        query = f"SELECT * FROM {table_name}"
        connection = db_connector.init_db_engine().connect()
        data = pd.read_sql(query, connection)
        return data

    def retrieve_pdf_data(self):
        file = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        card_details_list = tabula.read_pdf(file, lattice=True, pages = 'all')
        card_details = pd.concat(card_details_list,ignore_index=True)
        return card_details
    
    def api_details(self):
        self.number_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
        self.details_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}"
        self.headers = {"x-api-key" : "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
        
    def list_number_of_stores(self):
        response = requests.get(self.number_endpoint, headers=self.headers)
        return response.json()['number_stores']

    def retrieve_store_data(self, endpoint):
        number_of_stores = self.list_number_of_stores()
        store_data_list = []
        for store_number in range (0, number_of_stores):
                store_endpoint = endpoint.format(store_number=store_number)
                response = requests.get(store_endpoint, headers=self.headers)
                store_data = response.json()
                store_data_list.append(store_data)
        stores_df = pd.DataFrame(store_data_list)

        return stores_df

    def extract_from_s3(self):
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket = 'data-handling-public', Key = 'products.csv')
        s3_data = pd.read_csv(response['Body'])
        return s3_data

    def retrieve_events_data(self):
        url = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
        response = requests.get(url)
        json_response = response.json()
        df = pd.DataFrame(json_response)
        return df

