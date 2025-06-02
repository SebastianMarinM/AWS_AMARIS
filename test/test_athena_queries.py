
import pytest
from unittest.mock import patch, MagicMock
from scripts.query_data import AthenaQuerier

@patch('scripts.query_data.boto3.client')
def test_run_query_success(mock_boto_client):
    mock_athena = MagicMock()
    mock_boto_client.return_value = mock_athena

    mock_athena.start_query_execution.return_value = {'QueryExecutionId': '1234'}
    mock_athena.get_query_execution.return_value = {
        'QueryExecution': {'Status': {'State': 'SUCCEEDED'}}
    }
    mock_athena.get_query_results.return_value = {
        'ResultSet': {
            'ResultSetMetadata': {'ColumnInfo': [{'Label': 'col1'}]},
            'Rows': [{'Data': [{'VarCharValue': 'col1'}]}, {'Data': [{'VarCharValue': 'value1'}]}]
        }
    }

    querier = AthenaQuerier(database="test_db", s3_output_location="s3://test-bucket/results/")
    result = querier.run_query("SELECT * FROM test")
    assert not result.empty
