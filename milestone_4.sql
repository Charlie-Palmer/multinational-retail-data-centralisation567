--M4 Task 1 How many stores does the business have and in which countries?
SELECT country_code,
       COUNT(country_code) AS total_number_of_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_number_of_stores DESC; 

--M4 Task 2 Which locations currently have the most stores?
SELECT locality,
       COUNT(locality) AS total_number_of_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_number_of_stores DESC 
LIMIT 10;

--M4 Task 3 Which months produced the largest amount of sales
SELECT dim_date_times.month,
       SUM(orders_table.product_quantity * dim_products.product_price) AS "total_sales"
FROM orders_table
JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
JOIN dim_products on orders_table.product_code = dim_products.product_code
GROUP BY month
ORDER BY "total_sales" DESC
LIMIT 6; 

--M4 Task 4 How many sales are coming from online?
SELECT  COUNT(orders_table.store_code) numbers_of_sales,
        SUM(orders_table.product_quantity) AS product_quantity_count,
        CASE
            WHEN dim_store_details.store_type = 'Web Portal' THEN 'Web'
            ELSE 'Offline'
        END AS location_type
FROM orders_table
JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
GROUP BY location_type
ORDER BY product_quantity_count ASC; 

--M4 Task 5 What percentage of sales come through each type of store?
SELECT  dim_store_details.store_type,
        CAST(SUM(orders_table.product_quantity * dim_products.product_price) AS NUMERIC) AS total_sales,
        ROUND(CAST(SUM(orders_table.product_quantity * dim_products.product_price) AS NUMERIC) * 100.0 / CAST(SUM(SUM(orders_table.product_quantity * dim_products.product_price)) OVER() AS NUMERIC), 2) AS "sales_made(%)"
FROM dim_store_details
JOIN orders_table ON dim_store_details.store_code = orders_table.store_code 
JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY dim_store_details.store_type
ORDER BY total_sales DESC;

--M4 Task 6 Which month in each year produced the highest cost of sales?
SELECT  SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales,
        dim_date_times.year AS year,
        dim_date_times.month AS month
FROM orders_table
JOIN dim_products ON orders_table.product_code = dim_products.product_code
JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
GROUP BY year,
         month
ORDER BY total_sales DESC
LIMIT 10;

--M4 Task 7 What is our staff headcount?
SELECT  SUM(staff_numbers) AS total_staff_numbers,
        country_code AS country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC;

--M4 Task 8 Which German store type is selling the most?
SELECT  SUM(orders_table.product_quantity * dim_products.product_price) AS total_sales,
        dim_store_details.store_type AS store_type,
        dim_store_details.country_code AS country_code
FROM orders_table
JOIN dim_products ON orders_table.product_code = dim_products.product_code
JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code
WHERE dim_store_details.country_code = 'DE'
GROUP BY store_type, country_code
ORDER BY total_sales ASC;

--M4 Task 9 How quickly is the company making sales?
WITH date_times_cte AS (
    SELECT
        year,
        year || '-' || LPAD(month::TEXT, 2, '0') || '-' || LPAD(day::TEXT, 2, '0') || ' ' || timestamp AS full_timestamp
    FROM
        dim_date_times)
SELECT
    year,
    AVG(time_difference) AS average_time_taken
FROM (
    SELECT
        year,
        full_timestamp::timestamp,
        LEAD(full_timestamp::timestamp) OVER (ORDER BY full_timestamp::timestamp) AS next_complete_time,
        LEAD(full_timestamp::timestamp) OVER (ORDER BY full_timestamp::timestamp) - full_timestamp::timestamp AS time_difference
    FROM date_times_cte
) AS subquery
WHERE next_complete_time IS NOT NULL
GROUP BY year
ORDER BY average_time_taken DESC
LIMIT 5;


