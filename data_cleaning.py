import pandas as pd
import numpy as np
from dateutil.parser import parse

#Changes dates to datetime, any data that cannot be converted to datetime will be converted to NaT values
def parse_date(date_str):
            try:
                return pd.to_datetime(date_str, errors='coerce')
            except:
                try:
                    return pd.to_datetime(date_str, format='%B-%y-%d', errors='coerce')
                except: 
                    return pd.NaT

class DataCleaning:
    #Performs cleaning by removing null values and formatting the join date to datetime.
    def clean_user_data(self, user_data: pd.DataFrame):
        #Replace "NULL" with actual None type
        user_data.replace("NULL", pd.NA, inplace=True)
        #Changes join date to datetime in a specific format
        user_data['join_date'] = user_data['join_date'].apply(parse_date)        
        user_data['join_date'] = user_data['join_date'].dt.strftime('%Y-%m-%d')
        #Remove all null data
        user_data.dropna(inplace=True) 
        #Return cleaned user data   
        return user_data
     

    #Cleans card data removing null valus, duplicates, and changing confirmation date to specific format
    def clean_card_data(self, card_details: pd.DataFrame):
        # Replace "NULL" values with NaN (if needed)
        card_details.replace("NULL", pd.NA, inplace=True)
       
        # Convert 'card_number' to a string to avoid scientific notation
        card_details['card_number'] = card_details['card_number'].astype(str).str.strip()
        
        # Drop duplicate card numbers
        card_details.drop_duplicates(subset=['card_number'], keep='first', inplace=True)
        
        # Convert 'date_payment_confirmed' to datetime
        card_details['date_payment_confirmed'] = card_details['date_payment_confirmed'].apply(parse_date)
        card_details['date_payment_confirmed'] = card_details['date_payment_confirmed'].dt.strftime('%Y-%m-%d')
   
        #Drop all Na values
        card_details.dropna(inplace=True)
        # Return the cleaned data
        return card_details

    def clean_store_data(self, store_data:pd.DataFrame):
        #Drop 'lat' column as it contains no data
        store_data.drop(columns=['index', 'lat'], inplace=True)
        store_data.fillna('N/A', inplace=True)
        #Replace null values with Na
        store_data.replace("NULL", pd.NA, inplace=True)

        #Convert 'opening_date' to Date Time
        store_data['opening_date'] = store_data['opening_date'].apply(parse_date)
        store_data['opening_date'] = store_data['opening_date'].dt.strftime('%Y-%m-%d')
        
        #Strip away anything that isn't a number from 'staff_number'
        store_data['staff_numbers'] = store_data['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
        
        #Drop all Na values
        store_data.dropna(inplace=True)
        
        return store_data
    
    
    #Converts all data in the weight column to kg and removes any letters or punctuation
    def convert_product_weights(self, weight):
        if isinstance(weight, float):
            return weight
        #Deals with multipliers such as '4 x 100g'
        elif 'x' in weight: 
            quantity = float(weight.split('x')[0].strip())
            if 'g' in weight:
                weight = float(weight.split('x')[1].replace('g', '').strip())
            else:
                weight = float(weight.split('x')[1].strip())
            return (quantity * weight) / 1000
        #Deals with data containing trailing . such as '77g .'
        elif weight.endswith('.'):
            return float(weight.split(' ')[0].replace('g', '').strip()) / 1000
        #Converts data to kg and removes any letters
        elif 'ml' in weight:
            return float(weight.replace('ml', '')) / 1000
        elif 'kg' in weight:
            return float(weight.replace('kg', ''))
        elif 'g' in weight:
            return float(weight.replace('g', '')) / 1000
        elif 'oz' in weight:
            return float(weight.replace('oz', '')) *0.0283495
        #Any data that cannot be converted will be changed to NaN
        else:
            return np.nan
        
    def clean_products_data(self, product_data:pd.DataFrame):
        product_data.replace('NULL', pd.NA, inplace=True)
        product_data['weight'] = product_data['weight'].apply(self.convert_product_weights)
        product_data.dropna(inplace=True)
        return product_data
    
    def clean_orders_data(self, orders_data:pd.DataFrame):
        orders_data.drop(columns=['first_name', 'last_name', '1'])
        return orders_data
    
    def clean_events_data(self, events_data:pd.DataFrame):
        events_data.replace('NULL', pd.NA, inplace=True)
        for column in ['month', 'year', 'day']:
            events_data[column] = events_data[column].astype(str).str.replace(r'[^0-9]', '', regex=True)
            events_data[column] = pd.to_numeric(events_data[column], errors='coerce')

        events_data['date'] = pd.to_datetime(events_data[['day', 'month', 'year']], errors='coerce')
        events_data.dropna(inplace=True)

        events_data.reset_index(drop=True, inplace=True)
        return events_data

        