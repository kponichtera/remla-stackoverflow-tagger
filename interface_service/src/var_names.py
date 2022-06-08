"""A convenient way of accessing the
    names of commonly used environment vars.
"""

from enum import Enum


class VarNames(Enum):
    """Contains a mapping between environment variable
    names and their string representation, to avoid magic strings.
    """
    OBJECT_STORAGE_ENDPOINT = "OBJECT_STORAGE_ENDPOINT"
    OBJECT_STORAGE_ACCESS_KEY = "OBJECT_STORAGE_ACCESS_KEY"
    OBJECT_STORAGE_SECRET_KEY = "OBJECT_STORAGE_SECRET_KEY"
    OBJECT_STORAGE_TLS = "OBJECT_STORAGE_TLS"
    BUCKET_NAME = "BUCKET_NAME"
    MODEL_OBJECT_KEY = "MODEL_OBJECT_KEY"
    MODEL_LOCAL_PATH = "MODEL_LOCAL_PATH"
    PUBSUB_EMULATOR_HOST = "PUBSUB_EMULATOR_HOST"
    PUBSUB_PROJECT_ID = "PUBSUB_PROJECT_ID"
    PUBSUB_TOPIC_ID = "PUBSUB_TOPIC_ID"
    PUBSUB_SUBSCRIPTION_ID = "PUBSUB_SUBSCRIPTION_ID"
