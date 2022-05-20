import os
import pytest
import unittest
import pandas as pd

class DataTest(unittest.TestCase):
    """Testing basic main file"""
    
    @pytest.fixture(autouse=True)
    def prepare_fixture(self):
        """Fixture to generate test app."""
        dir_data = os.path.join(os.path.dirname(__file__), 'fake_data.csv')
        self.test_df = pd.read_csv(dir_data)
    
    def test_no_duplicates(self):
        self.assertEqual(len(self.test_df['id'].unique()), self.test_df.shape[0])
        self.assertEqual(self.test_df.groupby(['percentage','id']).size().max(), 1)
    
    def test_value_ranges(self):
        self.assertTrue((self.test_df['percentage']<=1).all())
        self.assertTrue((self.test_df.groupby('name')['budget'].sum() <= 1000).all())
        self.assertTrue(all (self.test_df['height']>=0))
