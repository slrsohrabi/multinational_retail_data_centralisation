# multinational_retail_data_centralisation
Consolidation into a single database for a multinational with sales data spread across multiple data sources for ease of analysis for company metrics.

# Table of Contents
1. [Introduction](#introduction)
2. [Data Extraction and Cleaning 1](#Data_Extraction_and_Cleaning_1)
    - [Data Extraction 1.1](#Data_Extraction_1.1)
    - [Data Cleaning 1.2](#Data_Cleaning_1.2)
3. [Licenses](#Licenses)


## Introduction
Content here...

## Data_Extraction_and_Cleaning_1
Utility class named DataExtractor is created in data_extraction.py for data extraction from various sources of CSV, an API, PDFs, RDS databases, and S3 buckets on AWS.

Utility class named DataCleaning is created in data_cleaning.py for cleaning user data, addresing issues such as handling NULL values, correcting date errors, ensuring proper data types, and filtering out erroneous information. Any file named like (dim_... .csv) is the cleaned version of the table.

Necessary libraries: pandas, numpy, tabula, requests, and boto3 , yaml, re.

### Data_Extraction_1.1
list_db_tables(self, table_name): Extracts data from an RDS database table specified by table_name.

read_rds_table(self, table_name): Reads data from an RDS database table specified by table_name and returns a pandas DataFrame.

retrieve_pdf_data(self, file_link): Extracts tabular data from a PDF file accessible via file_link and returns it as a pandas DataFrame.

list_number_of_stores(self, storenum_endp, header_dict): Retrieves store data from an API endpoint storenum_endp with custom headers specified in header_dict.

retrieve_stores_data(self, store_ret_end, header_dict): Fetches store data from an API endpoint store_ret_end with custom headers specified in header_dict.

extract_from_s3(self, bucket_name, object_key): Extracts data from a CSV file stored in an S3 bucket on AWS, specified by bucket_name and object_key.

### data_cleaning_1.2
clean_user_data(df): Cleans user data, handling NULL values, date errors, and incorrect types.

clean_card_data(df): Cleans card data, converting relevant columns to datetime format.

clean_store_data(df): Cleans store data, filtering, dropping columns, parsing datetime, and converting numeric values.

convert_product_weights(val): Converts product weights to a standardized format.

clean_product_data(df): Cleans product data, handling removed status, converting weight, and ensuring data consistency.

clean_orders_data(df): Cleans orders data by dropping specific columns and handling NULL values.

clean_date_details(df): Cleans date details by converting columns to numeric and combining them into a single datetime column.

## Licenses