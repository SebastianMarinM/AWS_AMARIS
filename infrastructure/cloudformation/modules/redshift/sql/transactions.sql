CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT,
    transaction_date TIMESTAMP,
    transaction_type VARCHAR(50),
    entity_id INT,
    quantity_kwh FLOAT,
    price_per_kwh FLOAT,
    energy_type VARCHAR(100),
    status VARCHAR(50),
    total_amount FLOAT,
    processing_timestamp TIMESTAMP,
    processing_date DATE,
    year INT,
    month INT,
    day INT
);