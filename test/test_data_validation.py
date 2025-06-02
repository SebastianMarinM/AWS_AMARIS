import unittest
import pandas as pd
from src.utils.helpers import validate_schema  # Assume helper script created

class TestDataValidation(unittest.TestCase):
    def test_validate_schema_pass(self):
        df = pd.DataFrame({'id': [1], 'name': ['X']})
        required_cols = ['id', 'name']
        self.assertTrue(validate_schema(df, required_cols))

    def test_validate_schema_fail(self):
        df = pd.DataFrame({'id': [1]})
        required_cols = ['id', 'name']
        self.assertFalse(validate_schema(df, required_cols))

if __name__ == '__main__':
    unittest.main()
