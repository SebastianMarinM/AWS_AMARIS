
-- Clientes por tipo y ciudad
SELECT 
    client_type, 
    city, 
    COUNT(DISTINCT client_id) AS client_count
FROM 
    processed_clients
GROUP BY 
    client_type, city
ORDER BY 
    client_count DESC;

-- Resumen de transacciones por tipo y energía
SELECT 
    transaction_type, 
    energy_type, 
    COUNT(*) AS transaction_count,
    SUM(quantity_kwh) AS total_energy,
    AVG(price_per_kwh) AS avg_price,
    SUM(total_amount) AS total_revenue
FROM 
    processed_transactions
GROUP BY 
    transaction_type, energy_type
ORDER BY 
    total_revenue DESC;


-- Proveedores por tipo de energía
SELECT 
    energy_type, 
    COUNT(DISTINCT provider_id) AS provider_count,
    AVG(capacity_mw) AS avg_capacity
FROM 
    processed_providers
GROUP BY 
    energy_type
ORDER BY 
    provider_count DESC;

-- Tendencia mensual de precios
SELECT 
    year, 
    month, 
    energy_type, 
    AVG(price_per_kwh) AS avg_price,
    SUM(quantity_kwh) AS total_energy
FROM 
    processed_transactions
GROUP BY 
    year, month, energy_type
ORDER BY 
    year DESC, month DESC;
