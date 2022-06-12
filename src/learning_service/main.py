"""Main file for the FastAPI application."""
import time
from fastapi import FastAPI
from google.cloud import pubsub_v1
from learning_service.config import settings
from common.color_module import ColorsPrinter
from prometheus_client import start_http_server
from learning_service.var_names import VarNames
from learning_service.text_classification import main
from google.cloud.pubsub_v1.subscriber.message import Message
from common.pubsub import subscribe_to_topic, publish_to_topic

def dummy_wait_and_send():
    """Stub method to publish a message.
    """
    time.sleep(5)
    # EVERYTHING must be a string
    data_to_publish = {
        "name": "bbe46356-2a38-4554-a18d-8a239bb742d0_model.joblib",
        "evaluation": str({
            "accuracy_score": 0.3419,
            "f1_score": 0.6530515001729919,
            "average_precision_score": 0.36209831252366137,
            "roc_auc": 0.9195568919487617
        })
    }
    app.publish_client.publish(
        app.publish_topic,
        b'New model data',
        **data_to_publish
    )

def receive_msg_callback(message : Message):
    """Acknowledges a Pub/Sub message. Used in the `subscribe()` function.

    Args:
        message (pubsub_v1.subscriber.message.Message): The message to acknowledge.
    """
    message.ack()
    ColorsPrinter.log_print_info(f'💬✔️ Received message: {message} ')
    dummy_wait_and_send()
    ColorsPrinter.log_print_info('Sent model! ✔️')


class LearningApp(FastAPI):
    """Learning FastAPI application

    Args:
        FastAPI (fastapi.FastAPI): FastAPI object
    """
    def __init__(self, *args, **kwargs):
        """Constructor for the Learning FastAPI application.
        """
        super().__init__(*args, **kwargs)
        pubsub_host = settings[VarNames.PUBSUB_EMULATOR_HOST.value]
        pubsub_project_id = settings[VarNames.PUBSUB_PROJECT_ID.value]
        pubsub_subscription_id = settings[VarNames.PUBSUB_SUBSCRIPTION_ID.value]

        pubsub_publish_topic_id = settings[VarNames.PUBSUB_MODEL_TOPIC_ID.value]
        pubsub_subscription_topic_id = settings[VarNames.PUBSUB_DATA_TOPIC_ID.value]

        subscriber, streaming_pull_future = subscribe_to_topic(
            pubsub_host,
            pubsub_project_id,
            pubsub_subscription_id,
            pubsub_subscription_topic_id,
            receive_msg_callback,
            unique_subscription_name=True
        )
        self.publish_topic = subscriber.topic_path(
            pubsub_project_id,
            pubsub_publish_topic_id
        )
        self.publish_client = publish_to_topic(self.publish_topic)
        self.subscribe_client = subscriber
        self.streaming_pull_future = streaming_pull_future
        self.title = "Learning Service API"
        self.description = "Learning Service API for learning models 📙🤖"
        self.version="0.0.1"
        start_http_server(9010)

app = LearningApp()

@app.get('/api/ping')
async def ping():
    """
    Used to test the connection.
    """
    return {}
