-- Vista: Análisis de Proveedores
CREATE OR REPLACE VIEW provider_analysis AS
SELECT 
    p.provider_id,
    p.provider_name,
    p.energy_type,
    p.capacity_mw,
    p.region AS location,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(CASE WHEN t.transaction_type = 'venta' THEN t.quantity_kwh ELSE 0 END) AS total_energy_sold,
    SUM(CASE WHEN t.transaction_type = 'compra' THEN t.quantity_kwh ELSE 0 END) AS total_energy_bought,
    AVG(t.price_per_kwh) AS avg_price_per_kwh
FROM 
    providers p
LEFT JOIN 
    transactions t 
    ON p.provider_id = t.entity_id
GROUP BY 
    p.provider_id, p.provider_name, p.energy_type, p.capacity_mw, p.region;

-- Vista: Análisis de Clientes
CREATE OR REPLACE VIEW customer_analysis AS
SELECT 
    c.client_id,
    c.client_name,
    c.client_type,
    c.city,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.quantity_kwh) AS total_energy_purchased,
    AVG(t.price_per_kwh) AS avg_price_per_kwh,
    SUM(t.total_amount) AS total_spent
FROM 
    clients c
LEFT JOIN 
    transactions t 
    ON c.client_id = t.entity_id AND t.transaction_type = 'venta'
GROUP BY 
    c.client_id, c.client_name, c.client_type, c.city;

-- Vista: Análisis de Precios por Tipo de Energía y Mes
CREATE OR REPLACE VIEW energy_type_analysis AS
SELECT 
    t.energy_type,
    t.transaction_type,
    DATE_TRUNC('month', t.transaction_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(t.quantity_kwh) AS total_energy,
    AVG(t.price_per_kwh) AS avg_price,
    MIN(t.price_per_kwh) AS min_price,
    MAX(t.price_per_kwh) AS max_price
FROM 
    transactions t
GROUP BY 
    t.energy_type, t.transaction_type, DATE_TRUNC('month', t.transaction_date);

