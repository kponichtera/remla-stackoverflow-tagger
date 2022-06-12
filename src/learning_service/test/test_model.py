import os
import pytest
import unittest
from joblib import load
from sklearn.metrics import r2_score


class ModelTest(unittest.TestCase):
    """Testing model related parameters"""

    def evaluate_score(self, classifier, validation_data):
        y_val = classifier.predict(self.input_data)
        y_true = validation_data
        return r2_score(y_true, y_val)

    @pytest.fixture(autouse=True)
    def prepare_fixture(self):
        """Fixture to generate test app."""
        base_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            ),
            "learning_service",
            "notebooks"
        )
        # TODO: these paths have to be changed later on when a proper workflow is set
        input_data_dir = os.path.join(base_dir, 'X_val_tfidf.joblib')
        validation_data_dir = os.path.join(base_dir, 'y_val.joblib')
        trained_model_dir = os.path.join(base_dir, 'classifier.joblib')
        self.input_data = load(input_data_dir)
        self.validation_data = load(validation_data_dir)
        self.trained_model = load(trained_model_dir)

    def test_data_stability(self):
        """Tests whether the latest generation of the model maintains an R2 score within a given range"""
        original_score = self.evaluate_score(self.trained_model, self.validation_data)
        assert original_score <= 0.5  # TODO: play with the parameter
