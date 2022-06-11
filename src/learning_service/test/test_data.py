import os
import pytest
import unittest
import tensorflow_data_validation as tfdv


class DataTest(unittest.TestCase):
    """Testing input data anomalies"""

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
            "data"
        )
        # TODO: these paths have to be changed later on when a proper workflow is set
        self.test_data_dir = os.path.join(base_dir, 'train.tsv')
        self.stats_options = tfdv.StatsOptions(enable_semantic_domain_stats=True)

    def test_no_anomalies(self):
        """Uses the tensorflow data validation library to look for anomalies in the train dataset"""
        train_stats = tfdv.generate_statistics_from_csv(self.test_data_dir, delimiter='\t',
                                                        stats_options=self.stats_options)
        schema = tfdv.infer_schema(statistics=train_stats)
        # all data points must contain a title and tags
        tfdv.get_feature(schema, 'title').presence.min_fraction = 1.0
        tfdv.get_feature(schema, 'tags').presence.min_fraction = 1.0
        anomalies = tfdv.validate_statistics(statistics=train_stats, schema=schema)
        assert 'anomaly_info' not in str(anomalies)
