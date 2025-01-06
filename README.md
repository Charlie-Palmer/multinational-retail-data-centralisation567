
# Multinational Retail Data Centralisation project

## Project description
In this project we are working for a multinational company selling various goods worldwide.
Currently their data is spread accross a variety of data sources. In order to make their data more easily accessible the company wants to centralise their data into one location.

The main objectives of this project were to:
1. Extract and clean all the data from a variety of sources.
2. Develop a star based schema ensuring all columns are of the correct data type.
3. Finally query the data to help the business make more data driven decisions.

#Installation instructions
1. Clone the repository `git clone https://github.com/Charlie-Palmer/multinational-retail-data-centralisation567`
2. Install the required packages `pip install -r requitements.txt`
3. Install SQL packages, this project uses PgAdmin 4, and SQL Tools in VSCode.

#Usage
Database credentials: ensure that the credentials for both the source and destination databases are correctly specified in the `db_creds.yaml` and `my_creds.yaml` files.

The `database_utils.py` file is be used to access a specified database which we are extracting data from, and upload data to a local database.

The `data_extraction.py` file is used to extract data from different sources in the database that we have accessed.

The `data_cleaning.py` file is used to clean the data that has been extracted. 

