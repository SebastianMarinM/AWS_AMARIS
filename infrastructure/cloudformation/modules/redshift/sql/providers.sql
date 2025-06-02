CREATE TABLE IF NOT EXISTS providers (
    provider_id INT,
    provider_name VARCHAR(255),
    energy_type VARCHAR(100),
    capacity_mw FLOAT,
    region VARCHAR(100),
    processing_timestamp TIMESTAMP,
    processing_date DATE
);