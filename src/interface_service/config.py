"""
Provides a configuration management object.
"""
from enum import Enum

from dynaconf import Dynaconf, Validator

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
    PUBSUB_DATA_TOPIC_ID = "PUBSUB_DATA_TOPIC_ID"
    PUBSUB_MODEL_TOPIC_ID = "PUBSUB_MODEL_TOPIC_ID"
    PUBSUB_SUBSCRIPTION_ID = "PUBSUB_SUBSCRIPTION_ID"


settings = Dynaconf(
    # variables exported in .env as `REMLA_FOO=bar` becomes `settings.FOO == "bar"`
    envvar_prefix="REMLA",
    load_dotenv=False,
    settings_files=['interface_service/configs/settings.yaml'],
    # Enable layered environments
    environments=True,
    # To switch environments `export REMLA_ENV=deployment`
    env_switcher="REMLA_ENV",
)

settings.validators.register(
    # Check that either the development or the deployment envs is active.
    Validator("env", is_in=["development", "deployment"]),

    Validator(VarNames.OBJECT_STORAGE_ENDPOINT.value, must_exist=True),
    Validator(VarNames.OBJECT_STORAGE_ACCESS_KEY.value, must_exist=True),
    Validator(VarNames.OBJECT_STORAGE_SECRET_KEY.value, must_exist=True),
    Validator(VarNames.OBJECT_STORAGE_TLS.value, default=False),
    Validator(VarNames.BUCKET_NAME.value, must_exist=True),
    Validator(VarNames.MODEL_OBJECT_KEY.value, must_exist=True),
    Validator(VarNames.MODEL_LOCAL_PATH.value, must_exist=True),

    Validator(VarNames.PUBSUB_EMULATOR_HOST.value, default=None),
    Validator(VarNames.PUBSUB_PROJECT_ID.value, must_exist=True),
    Validator(VarNames.PUBSUB_DATA_TOPIC_ID.value, must_exist=True),
    Validator(VarNames.PUBSUB_MODEL_TOPIC_ID.value, must_exist=True),
    Validator(VarNames.PUBSUB_SUBSCRIPTION_ID.value, must_exist=True),
)

settings.validators.validate()
