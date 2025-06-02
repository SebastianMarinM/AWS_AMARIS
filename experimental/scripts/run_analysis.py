import boto3
import pandas as pd
import time
import os
from datetime import datetime
from botocore.exceptions import ClientError

class AthenaAnalyzer:
    def __init__(self, database, output_bucket, region='us-east-1'):
        self.athena = boto3.client('athena', region_name=region)
        self.database = database
        self.output_path = f"s3://{output_bucket}/athena_results/"

    def run_query(self, query):
        try:
            response = self.athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={'OutputLocation': self.output_path}
            )
            execution_id = response['QueryExecutionId']
            return self._wait_and_process(execution_id)
        except ClientError as e:
            raise Exception(f"Athena error: {e}")

    def _wait_and_process(self, execution_id):
        while True:
            status = self.athena.get_query_execution(QueryExecutionId=execution_id)
            state = status['QueryExecution']['Status']['State']
            if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(2)

        if state != 'SUCCEEDED':
            reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown reason')
            raise Exception(f"Query failed: {reason}")

        results = self.athena.get_query_results(QueryExecutionId=execution_id)
        columns = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        rows = []
        for row in results['ResultSet']['Rows'][1:]:
            values = [field.get('VarCharValue', '') for field in row['Data']]
            rows.append(values)
        return pd.DataFrame(rows, columns=columns)

def main():
    database = "energy_processed"
    output_bucket = "your-energy-trading-datalake"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs("analysis_results", exist_ok=True)

    analyzer = AthenaAnalyzer(database, output_bucket)

    queries = {
        "customer_consumption": """
            SELECT client_type, city, COUNT(DISTINCT c.client_id) as clients,
                   SUM(t.total_amount) as total_spent
            FROM transactions t
            JOIN clients c ON t.entity_id = c.client_id
            WHERE transaction_type = 'venta'
            GROUP BY client_type, city
            ORDER BY total_spent DESC
        """,
        "provider_performance": """
            SELECT energy_type, COUNT(DISTINCT p.provider_id) as providers,
                   SUM(quantity_kwh) as total_energy, AVG(price_per_kwh) as avg_price
            FROM transactions t
            JOIN providers p ON t.entity_id = p.provider_id
            WHERE transaction_type = 'compra'
            GROUP BY energy_type
        """
    }

    for name, sql in queries.items():
        try:
            print(f"Running analysis: {name}")
            df = analyzer.run_query(sql)
            output_file = f"analysis_results/{name}_{timestamp}.csv"
            df.to_csv(output_file, index=False)
            print(f"Saved: {output_file}")
        except Exception as e:
            print(f"Error running {name}: {e}")

if __name__ == "__main__":
    main()
