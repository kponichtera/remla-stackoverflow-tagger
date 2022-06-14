"""Locust file for running load tests."""
import os
import random
from ast import literal_eval
import pandas as pd
from locust import HttpUser, task


predict_data = pd.read_csv(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "text_prepare_tests.tsv"),
    sep='\t',
    dtype={'title': 'str'}
)
predict_data = list(predict_data["title"].values)

correction_data = pd.read_csv(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation.tsv"),
    sep='\t',
    dtype={'title': 'str', 'tags': 'str'}
)
correction_data = correction_data[["title", "tags"]]
correction_data['tags'] = correction_data['tags'].apply(literal_eval)


class InferenceTest(HttpUser):
    """Interface locust test class.

    Args:
        HttpUser (locust.HttpUser): locust's HttpUser class
    """

    @task
    def ping_endpoint(self):
        """Ping request."""
        self.client.get("api/ping")
        
    @task
    def model_present(self):
        """Is model present request."""
        self.client.get("api/model_present")
        
    @task
    def predict(self):
        """Predict request."""
        self.client.post(
            "api/predict", json={
                "title": random.choice(predict_data)
            }
        )

    def correct(self):
        """Correct request."""
        df_correct = correction_data.sample()
        predicted = list(correction_data.sample()['tags'].values)
        self.client.post(
            "api/correct", json={
                "title": df_correct['title'].values[0],
                "predicted": predicted[0],
                "actual": df_correct['tags'].values[0]
            }
        )
