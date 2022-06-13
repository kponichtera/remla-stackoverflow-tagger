"""
Provides a configuration management object.
"""
from dynaconf import Dynaconf, Validator
from learning_service.var_names import VarNames

settings = Dynaconf(
    # variables exported in .env as `REMLA_FOO=bar` becomes `settings.FOO == "bar"`
    envvar_prefix="REMLA",
    load_dotenv=False,
    settings_files=['learning_service/configs/settings.yaml'],
    environments=True,
    env_switcher="REMLA_ENV",
)

settings.validators.register(
    # Check that either the development or the deployment envs is active.
    Validator("env", is_in=["development", "deployment"]),

    # Check that the necessary vars always exist in the development env.
    # These variables should be specified in the `configs/settings.yaml` file.
    Validator(VarNames.DATA_DIR.value, must_exist=True),
    Validator(VarNames.DATASET_FOR_TRAINING_DIR.value, must_exist=True),
    Validator(VarNames.OUTPUT_DIR.value, must_exist=True),
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
