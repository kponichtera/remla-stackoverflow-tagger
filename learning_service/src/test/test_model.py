import os
import pytest
import unittest
import pandas as pd

class ModelTest(unittest.TestCase):
    """Testing basic main file"""
    
    @pytest.fixture(autouse=True)
    def prepare_fixture(self):
        """Fixture to generate test app."""
        dir_data = os.path.join(os.path.dirname(__file__), 'fake_data.csv')
        self.test_data = pd.read_csv(dir_data)
        self.trained_model = joblib.load('trained_model.sav')
    
    def test_data_slice(self): 
        original_score = evaluate_score(self.trained_model, self.test_data)
        sliced_data = self.test_data[self.test_data['city'] == 'Delft']
        sliced_score = evaluate_score(self.trained_model, sliced_data)
        assert abs(original_score - sliced_data) <= 0.05
