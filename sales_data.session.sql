ALTER TABLE dim_users
ALTER COLUMN country_code TYPE VARCHAR(2) USING country_code::VARCHAR(2);

-- SELECT column_name,data_type
-- FROM
--     information_schema.columns
-- WHERE
--     table_name = 'dim_users'