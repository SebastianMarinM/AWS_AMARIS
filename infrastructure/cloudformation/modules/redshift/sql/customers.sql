CREATE TABLE IF NOT EXISTS customers (
    customer_id INT,
    id_type VARCHAR(50),
    id_number VARCHAR(50),
    customer_name VARCHAR(255),
    city VARCHAR(100),
    customer_type VARCHAR(100),
    registration_date DATE,
    processing_timestamp TIMESTAMP,
    processing_date DATE
);