import pandas as pd
import numpy as np
from datetime import datetime
import os

# Crear carpeta de salida si no existe
os.makedirs('data/raw', exist_ok=True)

# Fijar semilla para reproducibilidad
np.random.seed(42)

# ========================
# Generar Proveedores
# ========================
def generate_providers(n=50):
    energy_types = ['wind', 'hydro', 'nuclear']
    providers = {
        'provider_id': [f'PRV{i:03}' for i in range(1, n + 1)],
        'provider_name': [f'Provider_{i}' for i in range(1, n + 1)],
        'energy_type': np.random.choice(energy_types, size=n),
        'capacity_mw': np.random.uniform(100, 1000, n).round(2),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=n),
        'contract_start_date': pd.date_range(start='2022-01-01', periods=n, freq='D')
    }
    return pd.DataFrame(providers)

# ========================
# Generar Clientes
# ========================
def generate_customers(n=200):
    id_types = ['DNI', 'RUC', 'CE']
    cities = ['Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Piura']
    customers = {
        'client_id': [f'CLI{i:03}' for i in range(1, n + 1)],
        'id_type': np.random.choice(id_types, size=n),
        'identification': [f'{np.random.randint(10000000, 99999999)}' for _ in range(n)],
        'client_name': [f'Customer_{i}' for i in range(1, n + 1)],
        'city': np.random.choice(cities, size=n),
        'client_type': np.random.choice(['residential', 'commercial', 'industrial'], size=n),
        'contract_start_date': pd.date_range(start='2022-01-01', periods=n, freq='D')
    }
    return pd.DataFrame(customers)

# ========================
# Generar Transacciones
# ========================
def generate_transactions(n=1000):
    entity_ids = [f'PRV{i:03}' for i in range(1, 51)] + [f'CLI{i:03}' for i in range(1, 201)]
    transactions = {
        'transaction_id': [f'TRX{i:04}' for i in range(1, n + 1)],
        'transaction_date': pd.date_range(start='2023-01-01', periods=n, freq='H'),
        'transaction_type': np.random.choice(['compra', 'venta'], size=n),
        'entity_id': np.random.choice(entity_ids, size=n),
        'quantity_kwh': np.random.uniform(100, 10000, n).round(2),
        'price_per_kwh': np.random.uniform(0.05, 0.15, n).round(4),
        'energy_type': np.random.choice(['wind', 'hydro', 'nuclear'], size=n)
    }
    df = pd.DataFrame(transactions)
    df['total_amount'] = df['quantity_kwh'] * df['price_per_kwh']
    return df

# ========================
# Guardar CSVs
# ========================
timestamp = datetime.now().strftime('%Y%m%d')
generate_providers().to_csv(f'data/raw/providers_{timestamp}.csv', index=False)
generate_customers().to_csv(f'data/raw/clients_{timestamp}.csv', index=False)
generate_transactions().to_csv(f'data/raw/transactions_{timestamp}.csv', index=False)

print("✅ Sample data generated in 'data/raw/'")
