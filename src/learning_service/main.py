"""Main file for the FastAPI application."""
import os
import json
from fastapi import FastAPI
from threading import Thread
from learning_service.config import settings
from common.color_module import ColorsPrinter
from learning_service.var_names import VarNames
from learning_service.text_preprocessing import main as preprocess_main
from learning_service.text_classification import main as classification_main
from learning_service.get_data import copy_data
from learning_service.dir_util import get_directory_from_settings_or_default
from google.cloud.pubsub_v1.subscriber.message import Message
from common.pubsub import subscribe_to_topic, publish_to_topic
import prometheus_client


setting_dir = VarNames.OUTPUT_DIR
OUTPUT_PATH = get_directory_from_settings_or_default(
    setting_dir,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
)

def train_and_send():
    """Method to train and send a model.
    """
    copy_data()
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
    # EVERYTHING must be a string
    data_to_publish = { 
        "name": settings[VarNames.MODEL_OBJECT_KEY.value],
        "evaluation": str(evaluation_data)
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
    train_and_send()
    ColorsPrinter.log_print_info('Sent model! ✔️')


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
        self.version="0.0.1"

        prometheus_client.start_http_server(9010)
        
        # Create a new thread for the blockinb Pub/Sub call and start it
        pubsub_thread = Thread(target=get_result, args=(streaming_pull_future,))
        pubsub_thread.start()

app = LearningApp()

@app.get('/api/ping')
async def ping():
    """
    Used to test the connection.
    """
    return {}



@app.get('/api/learn')
async def learn():
    """
    Used to test the connection.
    """
    copy_data()
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

    data_to_publish = { 
        "name": settings[VarNames.MODEL_OBJECT_KEY.value],
        "evaluation": evaluation_data
    }
    app.publish_client.publish(
        app.publish_topic,
        b'New model data',
        **data_to_publish
    )
    return data_to_publish
