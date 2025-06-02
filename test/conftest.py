import pytest

@pytest.fixture
def sample_data():
    return [
        {"customer_id": "001", "customer_type": "residential", "city": "Lima"},
        {"customer_id": "002", "customer_type": "commercial", "city": "Cusco"}
    ]
