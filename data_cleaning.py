import pandas as pd
import numpy as np
from dateutil import parser

class DataCleaning:    
    #Changes dates to datetime, any data that cannot be converted to datetime will be converted to NaT values
    def clean_invalid_dates(self, df: pd.DataFrame, column_name):
        def parse_date(value):
            try:
                #Ensure the value is a string that looks like a date
                if isinstance(value, str) and any(char.isdigit() for char in value):
                    return parser.parse(value)
                else:
                    return pd.NaT
            except (ValueError, TypeError, parser.ParserError):
                return pd.NaT
        #Apply parse_date function to the desired column
        df[column_name] = df[column_name].apply(parse_date)
        #Change valid dates to the desired format, invalid dates are converted to NaT
        df[column_name] = df[column_name].apply(lambda x: x.strftime("%d-%m-%Y") if pd.notnull(x) else pd.NaT)       
        return df
        
    def remove_null(self, df: pd.DataFrame):
        df = df.replace("NULL", pd.NA)        
        return df    
    
    #Performs cleaning by removing null values and formatting the join date to datetime.
    def clean_user_data(self, user_data: pd.DataFrame):       
        user_data = self.remove_null(user_data)
        user_data = self.clean_invalid_dates(user_data, 'join_date')
        user_data = self.clean_invalid_dates(user_data, 'date_of_birth')      
        #Remove all null data
        user_data.dropna(inplace=True)
        #Return cleaned user data          
        return user_data
     
    #Cleans card data removing null values, duplicates, and changing confirmation date to specific format
    def clean_card_data(self, card_details: pd.DataFrame):
        card_details = self.remove_null(card_details)      
        card_details['card_number'] = card_details['card_number'].astype(str).str.strip()       
        card_details.drop_duplicates(subset=['card_number'], keep='first', inplace=True)
        card_details = self.clean_invalid_dates(card_details, 'date_payment_confirmed')
        card_details.dropna(inplace=True)
        return card_details
    
    #Cleans store data dropping unnecessary columns, removing symbols, letters, and blanks from the staff_numbers column
    def clean_store_data(self, store_data:pd.DataFrame):
        store_data.drop(columns=['index'], inplace=True)
        store_data = self.remove_null(store_data)
        store_data = self.clean_invalid_dates(store_data, 'opening_date')
        store_data['staff_numbers'] = store_data['staff_numbers'].str.replace(r'[^0-9]', '', regex=True)
        store_data.dropna(subset=['opening_date'], inplace=True)        
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
        
    #Cleans product data, removes null data and converts all weights to kg    
    def clean_products_data(self, product_data:pd.DataFrame):
        product_data = self.remove_null(product_data)
        product_data['weight'] = product_data['weight'].apply(self.convert_product_weights)
        product_data.dropna(inplace=True)
        return product_data
    
    #Drop unnecesary data in the orders table
    def clean_orders_data(self, orders_data:pd.DataFrame):
        orders_data.drop(columns=['first_name', 'last_name', '1', 'level_0', 'index'], inplace=True)       
        return orders_data
    
    #Cleans the events data by removing invalid dates from the year, month, and day columns. Removes any null values
    def clean_events_data(self, events_data:pd.DataFrame):
        events_data = self.remove_null(events_data)
        #Remove anything that is not a number then converts remaining data to numeric
        for column in ['month', 'year', 'day']:
            events_data[column] = events_data[column].astype(str).str.replace(r'[^0-9]', '', regex=True)
            events_data[column] = pd.to_numeric(events_data[column], errors='coerce')
        #Creates a date column to ensure remaining data contains only valid dates
        events_data['date'] = pd.to_datetime(events_data[['day', 'month', 'year']], errors='coerce')
        events_data.dropna(inplace=True)
        events_data.reset_index(drop=True, inplace=True)        
        return events_data

