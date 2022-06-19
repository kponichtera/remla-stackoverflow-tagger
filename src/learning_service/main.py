"""Main file for the FastAPI application."""
import json
import os
from threading import Thread, Lock

import prometheus_client
from fastapi import FastAPI
from google.cloud.pubsub_v1.subscriber.message import Message
from sklearn.multiclass import OneVsRestClassifier

from common.bucket import download_model, load_model
from common.logger import Logger
from common.pubsub import subscribe_to_topic, publish_to_topic
from learning_service.config import settings, VarNames
from learning_service.get_data import copy_data, copy_data_from_resources
from learning_service.text_classification import main as classification_main
from learning_service.text_preprocessing import main as preprocess_main, prepocess_incoming_data

OUTPUT_PATH = settings[VarNames.OUTPUT_DIR.value]

def train_and_send(app : FastAPI, train_file = "train.tsv", model = None):
    """Method to train and send a model.
    """
    copy_data()
    if model is None:
        preprocess_main(train_file=train_file)
    else:
        prepocess_incoming_data('/'.join(settings[VarNames.PREPROCESSOR_DATA_PATH.value].split('/')[:-1]),
                                '/'.join(settings[VarNames.PREPROCESSOR_LABELS_PATH.value].split('/')[:-1]),
                                settings[VarNames.PREPROCESSOR_LABELS_PATH.value].split('/')[-1],
                                train_file,
                                '/'.join(settings[VarNames.PUBSUB_DATA_TEMP_FILE.value].split('/')[:-1]))
    classification_main(bucket_upload=True, classifier=model)
    app.publish_client.publish(app.publish_topic, b'New model available')

def get_callback(lock : Lock, message_threshold : int, temp_file : str, train_file : str, app : FastAPI):
    """Generates a callback that processes the receives that by re-training

    Args:
        lock (Lock): The lock used to ensure atomic operations on the files and models
        message_threshold (int): The number of received messages required to trigger training
        temp_file (str): The file in which to temprarily store the received messages
        train_file (str): The file in which to move the messages for learning
    """

    def receive_msg_callback(message : Message):
        """Acknowledges a Pub/Sub message. Used in the `subscribe()` function.

        Args:
            message (pubsub_v1.subscriber.message.Message): The message to acknowledge.
        """
        message.ack()
        Logger.info(f'💬✔️ Received message: {message} ')
        lock.acquire()
        try:
            # Open the file and append to it
            if not (os.path.exists(temp_file) and os.path.isfile(temp_file)):
                with open(temp_file, 'w+') as f:
                    f.write("title\ttags\n")

            with open(temp_file, 'a') as f:
                tags = [tag[1:-1] for tag in message.attributes['actual'][1:-1].split(', ')]
                line = f'{message.attributes["title"]}\t{tags}'
                f.write(line + '\n')
            
            with open(temp_file, 'r') as f:
                lines = f.readlines()

            Logger.info(f'Wrote line {line} to {temp_file}. File now has {len(lines)} lines')

            # If the threshold has been reached, trigger re-learning
            if len(lines) >= message_threshold:
                # Perform learning
                train_and_send(app, temp_file.split('/')[-1], app.model)

                # Empty the temporary file
                with open(temp_file, 'w') as f:
                    f.write("title\ttags\n")
                
                Logger.info('Training')
                
        finally:
            lock.release()
        Logger.info('Sent model! ✔️')
    return receive_msg_callback

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

        self.lock = Lock()

        callback = get_callback(self.lock,
                                settings[VarNames.LEARNING_MESSAGE_THRESHOLD.value],
                                settings[VarNames.PUBSUB_DATA_TEMP_FILE.value],
                                settings[VarNames.DATA_DIR.value] + "/train.tsv",
                                self)

        subscriber, streaming_pull_future = subscribe_to_topic(
            pubsub_host,
            pubsub_project_id,
            pubsub_subscription_id,
            pubsub_subscription_topic_id,
            callback,
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
        # train_and_send(self)
        bucket_auth = (
            settings[VarNames.OBJECT_STORAGE_ACCESS_KEY.value],
            settings[VarNames.OBJECT_STORAGE_SECRET_KEY.value],
            settings[VarNames.OBJECT_STORAGE_TLS.value]
        )
        success = download_model(
            settings[VarNames.CLASSIFIER_LOCAL_PATH.value],
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.CLASSIFIER_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *bucket_auth
        )
        success = download_model(
            settings[VarNames.PREPROCESSOR_DATA_PATH.value],
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.PREPROCESSOR_DATA_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *bucket_auth
        )
        success = download_model(
            settings[VarNames.PREPROCESSOR_LABELS_PATH.value],
            settings[VarNames.BUCKET_NAME.value],
            settings[VarNames.PREPROCESSOR_LABELS_OBJECT_KEY.value],
            settings[VarNames.OBJECT_STORAGE_ENDPOINT.value],
            *bucket_auth
        )
        if success :
            self.model = load_model(settings[VarNames.CLASSIFIER_LOCAL_PATH.value])
        
        # Create a new thread for the blocking Pub/Sub call and start it
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
def learn():
    """
    Used to execute learning on the training data from the resources.
    """
    copy_data_from_resources()
    preprocess_main()
    app.model = classification_main(bucket_upload=True)
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
