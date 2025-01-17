
# Multinational Retail Data Centralisation

## Project Overview
This project focuses on centralizing retail data from various sources into a PostgreSQL database using a star schema. It involves extracting data, cleaning it, and loading it into a database for efficient storage and analysis. The project showcases data engineering skills, including ETL (Extract, Transform, Load) processes, database management, and SQL analysis.

## Features
-Data Extraction: Pulls raw data from multiple sources.
-Data Cleaning: Prepares and validates the data for consistency and accuracy.
-Data Loading: Centralizes the processed data into a PostgreSQL database.
-Data Analysis: Provides SQL queries for insights and metrics.

## Technologies Used
-Python: For scripting data extraction, transformation, and loading processes.
-PostgreSQL: As the database management system.
-Pandas: For data manipulation and cleaning.
-SQLAlchemy: For database interaction.
-YAML: For configuration management.
-pgAdmin 4: For managing and visualizing the PostgreSQL database.

## Prerequisites
1. Python 3.8 or higher
2. PostgreSQL 12 or higher
3. Required Python Packages: Install the packages listed in requirements.txt
   `pip install -r requitements.txt`
4. Database credentials: Ensure your database credentials are securely stored in a 'my_creds.yaml' file to access your local database, and 'db_creds.yaml' for the database you are extracting the data from.
   The layout of thes should be as follows:
   'my_creds.yaml'
   ```
   
   PG_USER: 'your username'
   PG_PASSWORD: 'your password'
   PG_HOST: 'your host name'
   PG_PORT: 'your port'
   PG_DATABASE: 'your database name'
   ```
   'db_creds.yaml'
   ```
   RDS_HOST: "host_address"
   RDS_PASSWORD: "password"
   RDS_USER: "username"
   RDS_DATABASE: "postgres"
   RDS_PORT: "portnumber"
   }
   ```
   
## Installation instructions
1. Clone the repository.
  `git clone https://github.com/Charlie-Palmer/multinational-retail-data-centralisation567`
2. Navigate to the project directory.
  `cd multinational-retail-data-centralisation567`
 
## SQL Scripts
The 'milestone_3.sql' file contains the scripts used to cast columns of the tables to the correct data types. Then the star based schema was created to be able to query the data and answer any questions the business has.
The queries can be found in the 'milestone_4.sql' file.


