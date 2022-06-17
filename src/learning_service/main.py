"""Main file for the FastAPI application."""
import json
import os
from threading import Thread

import prometheus_client
from fastapi import FastAPI
from google.cloud.pubsub_v1.subscriber.message import Message

from common.logger import Logger
from common.pubsub import subscribe_to_topic, publish_to_topic
from learning_service.config import settings, VarNames
from learning_service.get_data import copy_data, copy_data_from_resources
from learning_service.text_classification import main as classification_main
from learning_service.text_preprocessing import main as preprocess_main

OUTPUT_PATH = settings[VarNames.OUTPUT_DIR.value]

def train_and_send():
    """Method to train and send a model.
    """
    copy_data()
    preprocess_main()
    classification_main(bucket_upload=True)
    app.publish_client.publish(app.publish_topic, b'New model available')

def receive_msg_callback(message : Message):
    """Acknowledges a Pub/Sub message. Used in the `subscribe()` function.

    Args:
        message (pubsub_v1.subscriber.message.Message): The message to acknowledge.
    """
    message.ack()
    Logger.info(f'💬✔️ Received message: {message} ')
    train_and_send()
    Logger.info('Sent model! ✔️')


def get_result(streaming_pull_future):
    """Wrapper function for getting results from Pub/Sub.

    Args:
        streaming_pull_future: The stream from which to get the results.
    """
    streaming_pull_future.result()


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

        prometheus_client.start_http_server(9010)
        
        # Create a new thread for the blockinb Pub/Sub call and start it
        pubsub_thread = Thread(target=get_result, args=(streaming_pull_future,), daemon=True)
        pubsub_thread.start()

app = LearningApp()

@app.get('/api/ping')
def ping():
    """
    Used to test the connection.
    """
    return {}



@app.get('/api/learn')
<<<<<<< HEAD
async def learn():
=======
def learn():
>>>>>>> master
    """
    Used to execute learning on the training data from the resources.
    """
    copy_data_from_resources()
    preprocess_main()
    classification_main(bucket_upload=True)
    with open(
        os.path.join(
            OUTPUT_PATH,
            "evaluation.json"
        ),
        'r',
        encoding='utf-8'
        ) as f:
        evaluation_data = json.load(f)

    app.publish_client.publish(app.publish_topic, b'New model available')
    return {
        "name": settings[VarNames.MODEL_OBJECT_KEY.value],
        "evaluation": evaluation_data
    }
