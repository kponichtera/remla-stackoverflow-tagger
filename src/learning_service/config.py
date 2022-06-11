"""
Provides a configuration management object.
"""
from dynaconf import Dynaconf, Validator
from var_names import VarNames

settings = Dynaconf(
    # variables exported in .env as `REMLA_FOO=bar` becomes `settings.FOO == "bar"`
    envvar_prefix="REMLA",
    load_dotenv=False,
    settings_files=['src/configs/settings.yaml'],
    environments=True,
    env_switcher="DYNACONF_ENV",
)


settings.validators.register(
    # Check that either the development or the deployment envs is active.
    Validator("env", is_in=["development", "deployment"]),

    # Check that the necessary vars always exist in the development env.
    # These variables should be specified in the `configs/settings.yaml` file.
    Validator(VarNames.DATA_DIR.value,
              must_exist=True, env="development"),
    Validator(VarNames.DATASET_FOR_TRAINING_DIR.value,
              must_exist=True, env="development"),
    Validator(VarNames.OUTPUT_DIR.value,
              must_exist=True, env="development"),
    Validator(VarNames.OBJECT_STORAGE_ENDPOINT.value,
              must_exist=True, env="development"),
    Validator(VarNames.OBJECT_STORAGE_ACCESS_KEY.value,
              must_exist=True, env="development"),
    Validator(VarNames.OBJECT_STORAGE_TLS.value,
              must_exist=True, env="development"),
    Validator(VarNames.BUCKET_NAME.value, must_exist=True, env="development"),
    Validator(VarNames.MODEL_OBJECT_KEY.value,
              must_exist=True, env="development"),
    Validator(VarNames.MODEL_LOCAL_PATH.value,
              must_exist=True, env="development"),

    # Check that the necessary vars exist
    # In the deployment env when it is active.
    # These variables should be specified
    # As (standard) env variables.
    Validator(VarNames.DATA_DIR.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.DATASET_FOR_TRAINING_DIR.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.OUTPUT_DIR.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.OBJECT_STORAGE_ENDPOINT.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.OBJECT_STORAGE_ACCESS_KEY.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.OBJECT_STORAGE_TLS.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.BUCKET_NAME.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.MODEL_OBJECT_KEY.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
    Validator(VarNames.MODEL_LOCAL_PATH.value, must_exist=True, env="deployment",
              when=Validator("env", eq="deployment", must_exist=True)),
)

settings.validators.validate()
