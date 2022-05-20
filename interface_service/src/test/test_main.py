import pytest
import unittest
from src.main import app
from fastapi.testclient import TestClient

class MainTest(unittest.TestCase):
    """Testing basic main file"""
    
    @pytest.fixture(autouse=True, scope="module")
    def prepare_fixture(self):
        """Fixture to generate test app."""
        self.test_app = TestClient(app)
        
    def test_predict_main(self):
        """Predict test."""
        title = 'lol'
        response = self.test_app.post("/predict", params={"title": title})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result": ["java", "OOP"],
            "classifier": "decision tree",
            "title": title,
        })
