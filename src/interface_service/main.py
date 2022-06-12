"""Main file for the FastAPI application."""
from typing import Set
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud.pubsub_v1.subscriber.message import Message

from interface_service.config import settings
from interface_service.var_names import VarNames

from common.color_module import ColorsPrinter
from common.pubsub import subscribe_to_topic, publish_to_topic

def receive_msg_callback(message : Message):
    """Acknowledges a Pub/Sub message. Used in the `subscribe()` function.

    Args:
        message (pubsub_v1.subscriber.message.Message): The message to acknowledge.
    """
    message.ack()
    ColorsPrinter.log_print_info(f'💬✔️ Received message: {message} ')


class InferenceApp(FastAPI):
    """Inference FastAPI application

    Args:
        FastAPI (fastapi.FastAPI): FastAPI object
    """
    def __init__(self, *args, **kwargs):
        """Constructor for the Inference FastAPI application.
        """
        super().__init__(*args, **kwargs)
        pubsub_host = settings[VarNames.PUBSUB_EMULATOR_HOST.value]
        pubsub_project_id = settings[VarNames.PUBSUB_PROJECT_ID.value]
        pubsub_subscription_id = settings[VarNames.PUBSUB_SUBSCRIPTION_ID.value]

        pubsub_publish_topic_id = settings[VarNames.PUBSUB_DATA_TOPIC_ID.value]
        pubsub_subscription_topic_id = settings[VarNames.PUBSUB_MODEL_TOPIC_ID.value]

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
        self.title = "Inference Service API"
        self.description = "Inference Service API for accessing models 🚀"
        self.version="0.0.1"

app = InferenceApp()

@app.get('/api/ping')
async def ping():
    """
    Used to test the connection.
    """
    return {}


class PredictionRequest(BaseModel):
    """
    Defines the model of a prediction request.
    """
    title: str


class PredictionResult(BaseModel):
    """
    Defines the model of a prediction result.
    """
    title: str
    classifier: str
    tags: Set[str]


@app.post('/api/predict')
async def predict_tags(request: PredictionRequest):
    """
    Create a prediction of tags for the given StackOverflow title.

    - **title**: title of the StackOverflow question
    """
    return PredictionResult(
        title=request.title,
        classifier="decision tree",
        tags=["java", "OOP"],
    )


class CorrectionRequest(BaseModel):
    """Model for tag correction for a given title.

    Args:
        BaseModel (_type_): pydantic's base model class
    """
    title: str
    predicted: Set[str]
    actual: Set[str]


@app.post('/api/correct', summary="Correct the tags to the model", )
async def correct_prediction(request: CorrectionRequest):
    """
    Correct a prediction of tags for models to learn in the future.

    - **title**: title of the StackOverflow question
    - **predicted**: prediction of tags for the title
    - **actual**: actual tags for the title
    """
    data_to_publish = request.dict()
    data_to_publish["predicted"] = str(data_to_publish["predicted"])
    data_to_publish["actual"] = str(data_to_publish["actual"])
    app.publish_client.publish(
        app.publish_topic,
        b'New correction data',
        **data_to_publish
    )
    return request
