from typing import Set
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Interface Service API",
    description="Interface Service API for accessing models 🚀",
    version="0.0.1",
)


@app.post('/predict')
async def predict_tags(title : str, summary="Predict tags for StackOverflow title"):
    """
    Create a prediction of tags for the given StackOverflow title.

    - **title**: title of the StackOverflow question
    """
    return {
        "result": ["java", "OOP"],
        "classifier": "decision tree",
        "title": title,
    }


class Correction(BaseModel):
    title: str
    predicted: Set[str]
    actual: Set[str]


@app.post('/correct',
        response_model=Correction,
        summary="Correct the tags to the model",)
def correct_prediction(correction : Correction):
    """
    Correct a prediction of tags for models to learn in the future.

    - **title**: title of the StackOverflow question
    - **predicted**: prediction of tags for the title
    - **actual**: actual tags for the title
    """
    return correction
