"""Main file for the FastAPI application."""
from typing import Set

from fastapi import FastAPI
from pydantic import BaseModel
from src.pubsub import subscribe_to_topic, publish_to_topic
from src.var_names import VarNames
from src.config import settings
from src.bucket import download_model, load_model


class InferenceApp(FastAPI):
    """Inference FastAPI application

    Args:
        FastAPI (fastapi.FastAPI): FastAPI object
    """
    def __init__(self, *args, **kwargs):
        """Constructor for the Inference FastAPI application.
        """
        super().__init__(*args, **kwargs)
        subscriber, streaming_pull_future = subscribe_to_topic(unique_subscription_name=True)
        self.publish_topic = subscriber.topic_path(
            settings[VarNames.PUBSUB_PROJECT_ID.value],
            settings[VarNames.PUBSUB_DATA_TOPIC_ID.value])
        self.publish_client = publish_to_topic(self.publish_topic)
        self.subscribe_client = subscriber
        self.streaming_pull_future = streaming_pull_future
        self.title = "Inference Service API"
        self.description = "Inference Service API for accessing models 🚀"
        self.version = "0.0.1"
        download_model()
        self.model = load_model()

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

@app.post('/api/update', summary='Pull new model from the bucket')
async def update_model():
    """Update the internal model by pulling from object sotrage.
    """
    download_model()
    app.model = load_model()
