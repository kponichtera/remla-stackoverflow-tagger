"""Main file for the FastAPI application."""
import time
from fastapi import FastAPI
from src.var_names import VarNames
from src.config import settings
from src.pubsub import subscribe_to_topic, publish_to_topic

def dummy_wait_and_send():
    """Stub method to publish a message.
    """
    time.sleep(5)
    # EVERYTHING must be a string
    data_to_publish = {
        "name": "bbe46356-2a38-4554-a18d-8a239bb742d0_model.joblib",
        "evaluation": str({
            "accuracy_score": str(0.3419),
            "f1_score": str(0.6530515001729919),
            "average_precision_score": str(0.36209831252366137),
            "roc_auc": str(0.9195568919487617)
        })
    }
    app.publish_client.publish(
        app.publish_topic,
        b'New model data',
        **data_to_publish
    )


class LearningApp(FastAPI):
    """Learning FastAPI application

    Args:
        FastAPI (fastapi.FastAPI): FastAPI object
    """
    def __init__(self, *args, **kwargs):
        """Constructor for the Learning FastAPI application.
        """
        super().__init__(*args, **kwargs)
        subscriber, streaming_pull_future = subscribe_to_topic(
            unique_subscription_name=True,
            send_callback=dummy_wait_and_send
        )
        self.pubsub_project_id = settings[VarNames.PUBSUB_PROJECT_ID.value]
        self.pubsub_model_topic_id = settings[VarNames.PUBSUB_MODEL_TOPIC_ID.value]
        self.publish_topic = subscriber.topic_path(
            self.pubsub_project_id,
            self.pubsub_model_topic_id
        )
        self.publish_client = publish_to_topic(self.publish_topic)
        self.subscribe_client = subscriber
        self.streaming_pull_future = streaming_pull_future
        self.title = "Learning Service API"
        self.description = "Learning Service API for learning models 📙🤖"
        self.version="0.0.1"

app = LearningApp()

@app.get('/api/ping')
async def ping():
    """
    Used to test the connection.
    """
    return {}
