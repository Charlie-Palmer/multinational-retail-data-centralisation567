--M3 TASK 1
SELECT
    MAX(LENGTH(card_number)) AS max_card_number_length,
    MAX(LENGTH(store_code)) AS max_store_code_length,
    MAX(LENGTH(product_code)) AS max_product_code_length
FROM
    orders_table;
ALTER TABLE orders_table
    ALTER COLUMN date_uuid TYPE uuid USING date_uuid::UUID,
    ALTER COLUMN user_uuid TYPE uuid USING user_uuid::UUID,
    ALTER COLUMN card_number TYPE varchar(19),
    ALTER COLUMN store_code TYPE varchar(12),
    ALTER COLUMN product_code TYPE varchar(11),
    ALTER COLUMN product_quantity TYPE smallint;

--M3 TASK 2
SELECT
    MAX(LENGTH(country_code)) AS max_country_code_length
FROM    
    dim_users;

ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE varchar(255),
    ALTER COLUMN last_name TYPE varchar(255),
    ALTER COLUMN date_of_birth TYPE date USING date_of_birth::date,
    ALTER COLUMN country_code TYPE varchar(3),
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid,
    ALTER COLUMN join_date TYPE date USING join_date::date; 

--M3 TASK 3
UPDATE dim_store_details
SET latitude = COALESCE(latitude, lat);

ALTER TABLE dim_store_details
DROP COLUMN lat;

SELECT 
    MAX(LENGTH(store_code)) AS max_store_code_length,
    MAX(LENGTH(country_code)) AS max_country_code_length
FROM dim_store_details;

UPDATE dim_store_details
SET address = NULL,
    longitude = NULL,
    locality = NULL,
    latitude = NULL
WHERE address ='N/A' OR  longitude ='N/A' OR locality = 'N/A' OR latitude = 'N/A';

UPDATE dim_store_details
SET longitude = NULL
WHERE longitude ~ '[^0-9\.-]';

ALTER TABLE dim_store_details
    ALTER COLUMN longitude TYPE NUMERIC USING longitude :: NUMERIC,
    ALTER COLUMN locality TYPE varchar(255),
    ALTER COLUMN store_code TYPE varchar(12),
    ALTER COLUMN staff_numbers TYPE smallint USING staff_numbers :: smallint,
    ALTER COLUMN opening_date TYPE DATE USING opening_date :: DATE,
    ALTER COLUMN store_type TYPE varchar(255),
    ALTER COLUMN store_type DROP NOT NULL,
    ALTER COLUMN latitude TYPE NUMERIC USING latitude :: NUMERIC,
    ALTER COLUMN country_code TYPE varchar(3),
    ALTER COLUMN continent TYPE varchar(255);

--M3 TASK 4
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(20);

UPDATE dim_products
SET weight_class =
    CASE 
        WHEN weight <2 THEN 'Light'
        WHEN weight >=2 AND weight <40 THEN 'Mid_Sized'
        WHEN weight >=40 AND weight <140 THEN 'Heavy'
        WHEN weight >=140 THEN 'Truck_Required'
    END;

--M3 TASK 5
SELECT
    MAX(LENGTH("EAN")) AS max_length_ean,
    MAX(LENGTH(product_code)) AS max_product_code_length,
    MAX(LENGTH("weight_class")) AS max_weight_class_length
FROM dim_products;

ALTER TABLE dim_products
    RENAME removed TO still_available;

UPDATE dim_products
SET still_available =
    CASE 
        WHEN still_available = 'Still_avaliable' THEN TRUE
        WHEN still_available = 'Removed' THEN FALSE
    END;

ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE NUMERIC USING product_price :: NUMERIC,
    ALTER COLUMN weight TYPE NUMERIC USING weight :: NUMERIC,
    ALTER COLUMN "EAN" TYPE VARCHAR(17),
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN date_added TYPE DATE USING date_added :: DATE,
    ALTER COLUMN uuid TYPE UUID USING uuid :: UUID,
    ALTER COLUMN still_available TYPE BOOL USING still_available :: BOOL,
    ALTER COLUMN "weight_class" TYPE VARCHAR(14);

--M3 TASK 6
SELECT
    MAX(LENGTH(month)) AS max_length_month,
    MAX(LENGTH(year)) AS max_length_year,
    MAX(LENGTH(day)) AS max_length_day,
    MAX(LENGTH(time_period)) AS max_length_timestamp
FROM dim_date_times;

ALTER TABLE dim_date_times
    DROP COLUMN date,
    ALTER COLUMN month TYPE TEXT,
    ALTER COLUMN year TYPE TEXT,
    ALTER COLUMN day TYPE TEXT,
    ALTER COLUMN time_period TYPE TEXT;

ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE VARCHAR(2),
    ALTER COLUMN year TYPE VARCHAR(4),
    ALTER COLUMN day TYPE VARCHAR(2),
    ALTER COLUMN time_period TYPE VARCHAR(10),
    ALTER COLUMN date_uuid TYPE UUID USING date_uuid :: UUID;

--M3 TASK 7
SELECT
    MAX(LENGTH(card_number)) AS card_number,
    MAX(LENGTH(expiry_date)) AS expiry_date,
    MAX(LENGTH(date_payment_confirmed)) AS date_payment_confirmed
FROM dim_card_details;

ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE VARCHAR(22),
    ALTER COLUMN expiry_date TYPE VARCHAR(5),
    ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed :: DATE;

--M3 TASK 8
ALTER TABLE dim_users
    ADD CONSTRAINT pk_users PRIMARY KEY (user_uuid);

ALTER TABLE dim_store_details
    ADD CONSTRAINT pk_store_details PRIMARY KEY (store_code);

ALTER TABLE dim_products
    ADD CONSTRAINT pk_products PRIMARY KEY (product_code);

ALTER TABLE dim_date_times
    ADD CONSTRAINT pk_date_times PRIMARY KEY (date_uuid);

ALTER TABLE dim_card_details
    ADD CONSTRAINT pk_card_details PRIMARY KEY (card_number);

--M3 TASK 9
ALTER TABLE orders_table
ADD CONSTRAINT fk_user_uuid
FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT fk_store_code
FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);

ALTER TABLE orders_table
ADD CONSTRAINT fk_product_code
FOREIGN KEY (product_code) REFERENCES dim_products(product_code);

ALTER TABLE orders_table
ADD CONSTRAINT fk_date_uuid
FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT fk_card_number
FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);

