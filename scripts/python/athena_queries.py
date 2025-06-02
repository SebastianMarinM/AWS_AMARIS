import boto3
import time
import pandas as pd
from botocore.exceptions import ClientError


class AthenaClient:
    def __init__(self, database, s3_output_location, region_name='us-east-1'):
        self.athena = boto3.client('athena', region_name=region_name)
        self.s3_output_location = s3_output_location
        self.database = database

    def run_query(self, query):
        try:
            response = self.athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={'OutputLocation': self.s3_output_location}
            )
            query_execution_id = response['QueryExecutionId']

            # Wait for query to complete
            while True:
                status = self.athena.get_query_execution(QueryExecutionId=query_execution_id)
                state = status['QueryExecution']['Status']['State']
                if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(2)

            if state != 'SUCCEEDED':
                reason = status['QueryExecution']['Status'].get('StateChangeReason', 'No reason found')
                raise Exception(f"Query failed: {reason}")

            return self._process_results(query_execution_id)

        except ClientError as e:
            raise Exception(f"AWS Client Error: {e}")

    def _process_results(self, query_execution_id):
        result = self.athena.get_query_results(QueryExecutionId=query_execution_id)
        columns = [col['Label'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        rows = []
        for row in result['ResultSet']['Rows'][1:]:  # skip header
            values = [col.get('VarCharValue', None) for col in row['Data']]
            rows.append(dict(zip(columns, values)))
        return pd.DataFrame(rows)


def main():
    athena_client = AthenaClient(
        database='energy_processed',
        s3_output_location='s3://energy-trading-athena-results/output/'

    )

    queries = {
        'total_energy_by_type': """
            SELECT 
                energy_type,
                SUM(quantity_kwh) as total_energy,
                AVG(price_per_kwh) as avg_price
            FROM transactions
            WHERE transaction_type = 'venta'
            GROUP BY energy_type
            ORDER BY total_energy DESC
        """,

        'top_clients': """
            SELECT 
                c.client_name,
                c.client_type,
                COUNT(*) as transaction_count,
                SUM(t.quantity_kwh) as total_energy_consumed,
                SUM(t.total_amount) as total_spent
            FROM transactions t
            JOIN clients c ON t.entity_id = c.client_id
            WHERE t.transaction_type = 'venta'
            GROUP BY c.client_name, c.client_type
            ORDER BY total_spent DESC
            LIMIT 10
        """,

        'provider_performance': """
            SELECT 
                p.provider_name,
                p.energy_type,
                COUNT(*) as sales_count,
                SUM(t.quantity_kwh) as total_energy_sold,
                AVG(t.price_per_kwh) as avg_price
            FROM transactions t
            JOIN providers p ON t.entity_id = p.provider_id
            WHERE t.transaction_type = 'compra'
            GROUP BY p.provider_name, p.energy_type
            ORDER BY total_energy_sold DESC
        """
    }

    for name, query in queries.items():
        print(f"Running query: {name}")
        try:
            df = athena_client.run_query(query)
            print(df.head())
        except Exception as e:
            print(f"Error running {name}: {e}")


if __name__ == "__main__":
    main()