"""Basic test for inference service."""
import unittest
import pytest
from fastapi.testclient import TestClient
from interface_service.main import app

class MainTest(unittest.TestCase):
    """Testing basic main file"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_app = None

    @pytest.fixture(autouse=True, scope="module")
    def prepare_fixture(self):
        """Fixture to generate test app."""
        self.test_app = TestClient(app)

    @pytest.mark.skip(reason="The code is currently not mocking the logic behind the web server's callback")
    def test_predict_main(self):
        """Predict test."""
        title = 'lol'
        response = self.test_app.post("/api/predict", params={"title": title})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "result": ["java", "OOP"],
            "classifier": "decision tree",
            "title": title,
        })
