"""Basic test for inference service."""
import unittest
import pytest
#from fastapi.testclient import TestClient
#from learning_service.main import app

class MainTest(unittest.TestCase):
    """Testing basic main file"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_app = None

    """@pytest.fixture(autouse=True, scope="module")
    def prepare_fixture(self):
        self.test_app = TestClient(app)
    """

    @pytest.mark.skip(reason="Requires Google pub sub to be active.")
    def test_ping_main(self):
        """Ping test."""
        response = self.test_app.get("/api/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})
