
# Multinational Retail Data Centralisation

## Table of contents
1. [Project Overview](#ProjectOverview)
2. [Technologies Used](#TechnologiesUsed)
3. [Prerequisites](#Prerequisites)
4. [Installation And Usage Instructions](#InstallationAndUsageInstructions)
5. [File Structure](#FileStructure)
6. [Contributing](#Contributing)
7. [License](#License)

## Project Overview
This project focuses on centralizing retail data from various sources into a PostgreSQL database using a star schema. It involves extracting data, cleaning it, and loading it into a database for efficient storage and analysis. The project showcases data engineering skills, including ETL (Extract, Transform, Load) processes, database management, and SQL analysis.

## Technologies Used
- **Python:** For scripting data extraction, transformation, and loading processes.
- **PostgreSQL:** As the database management system.
- **Pandas:** For data manipulation and cleaning.
- **SQLAlchemy:** For database interaction.
- **YAML:** For configuration management.
- **pgAdmin 4:** For managing and visualizing the PostgreSQL database.

## Prerequisites
1. **Python 3.8 or higher**
2. **PostgreSQL 12 or higher**
3. **Required Python Packages:** Install the packages listed in `requirements.txt`
   ```bash
   pip install -r requirements.txt
   ```
4. **Database Credentials:** Ensure your database credentials are securely stored in a `my_creds.yaml` file to access your local database, and `db_creds.yaml` for the database you are extracting the data from. You should set up an empty database in pgadmin named 'sales_data' to be able to run the code given.

   The layout of these should be as follows:

   `my_creds.yaml`
   ```yaml
   PG_USER: 'your username'
   PG_PASSWORD: 'your password'
   PG_HOST: 'your host name'
   PG_PORT: 'your port'
   PG_DATABASE: 'your database name'
   ```

   `db_creds.yaml`
   ```yaml
   RDS_HOST: 'host_address'
   RDS_PASSWORD: 'password'
   RDS_USER: 'username'
   RDS_DATABASE: 'postgres'
   RDS_PORT: 'portnumber'
   ```

## Installation And Usage Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Charlie-Palmer/multinational-retail-data-centralisation567
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd multinational-retail-data-centralisation567
   ```
3. **Extracting the data:**
   Run methods in the `data_extraction.py` file to extract the necessary data.
4. **Clean the data:**
   With the dataframe you have extracted, run the appropriate methods in the `data_cleaning.py` file.
5. **Upload the data:**
   Run the 'upload_to_db' method in the `database_utils.py` file with your now clean dataframe. You will need to specify the name of the table you will be uploading to.

Here is an example of how you could carry out these steps using python.
   ```python
   from data_extraction import DataExtractor
   from data_cleaning import DataCleaning
   from database_utils import DatabaseConnector
   
   db_connector = DatabaseConnector()
   extractor = DataExtractor()
   cleaner = DataCleaning()

   events_data = extractor.retrieve_events_data()
   clean_events_data = cleaner.clean_events_data(events_data)
   db_connector.upload_to_db(clean_events_data, 'dim_date_times')
   ```

## File Structure
- `database_utils.py`: Class to connect with and upload to the database
- `data_exctraction.py`: Class to extract data from the various sources
- `data_cleaning.py`: Class to clean the data once extracted
- `milestone_3.sql`: Code used to ensure the data types were correct and to develop a star based schema
- `milestone_4.sql`: Code used to query the data and answer various business related questions
- `requirements.txt`: List of Python dependencies

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch: git checkout -b feature-name.
3. Commit changes: git commit -m 'Add feature name'.
4. Push to the branch: git push origin feature-name.
5. Submit a pull request.

## License
This project is licensed under the [MIT License](./LICENSE). See the `LICENSE` file for more details.
