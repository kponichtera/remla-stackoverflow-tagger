"""Main file for the FastAPI application."""
from typing import Set

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Interface Service API",
    description="Interface Service API for accessing models 🚀",
    version="0.0.1",
)


@app.get('/api/ping')
async def ping():
    return {}


class PredictionRequest(BaseModel):
    title: str


class PredictionResult(BaseModel):
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


@app.post('/api/correct', summary="Correct the tags to the model",)
def correct_prediction(request: CorrectionRequest):
    """
    Correct a prediction of tags for models to learn in the future.

    - **title**: title of the StackOverflow question
    - **predicted**: prediction of tags for the title
    - **actual**: actual tags for the title
    """
    return
