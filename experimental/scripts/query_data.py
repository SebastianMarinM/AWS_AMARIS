import boto3
import time
import pandas as pd
from botocore.exceptions import ClientError

class AthenaQuerier:
    def __init__(self, database, s3_output_location, region='us-east-1'):
        self.athena_client = boto3.client('athena', region_name=region)
        self.database = database
        self.s3_output_location = s3_output_location

    def run_query(self, query):
        try:
            response = self.athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={'OutputLocation': self.s3_output_location}
            )
            execution_id = response['QueryExecutionId']

            # Espera hasta que la consulta finalice
            while True:
                status = self.athena_client.get_query_execution(QueryExecutionId=execution_id)
                state = status['QueryExecution']['Status']['State']
                if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(2)

            if state != 'SUCCEEDED':
                reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
                raise Exception(f"Query failed: {reason}")

            return self._process_results(execution_id)

        except ClientError as e:
            raise Exception(f"Athena client error: {str(e)}")

    def _process_results(self, execution_id):
        results = self.athena_client.get_query_results(QueryExecutionId=execution_id)
        columns = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        rows = []
        for row in results['ResultSet']['Rows'][1:]:  # omitir encabezado
            values = [field.get('VarCharValue', '') for field in row['Data']]
            rows.append(values)
        return pd.DataFrame(rows, columns=columns)

def main():
    querier = AthenaQuerier(
        database='energy_processed',
        s3_output_location='s3://your-athena-output-bucket/results/'
    )

    queries = {
        'provider_summary': '''
            SELECT energy_type, COUNT(*) AS provider_count, AVG(capacity_mw) AS avg_capacity
            FROM providers
            GROUP BY energy_type
        ''',
        'transaction_summary': '''
            SELECT transaction_type, energy_type, COUNT(*) AS transaction_count,
                   SUM(quantity_kwh) AS total_kwh, AVG(price_per_kwh) AS avg_price
            FROM transactions
            GROUP BY transaction_type, energy_type
        ''',
        'customer_transactions': '''
            SELECT client_type, city, COUNT(*) AS transaction_count, SUM(total_amount) AS total_spent
            FROM transactions t
            JOIN clients c ON t.entity_id = c.client_id
            WHERE transaction_type = 'venta'
            GROUP BY client_type, city
        '''
    }

    for name, query in queries.items():
        print(f"Executing query: {name}")
        try:
            df = querier.run_query(query)
            print(df.head())
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
