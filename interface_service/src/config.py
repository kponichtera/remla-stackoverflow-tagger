
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="REMLA",               # variables exported in .env as `REMLA_FOO=bar` becomes `settings.FOO == "bar"`
    settings_files=['config/settings.yaml', 'config/.secrets.yaml'],
    environments=True,                   # Enable layered environments
    load_dotenv=True,
    env_switcher="DYNACONF_ENV",         # to switch environments `export ENV_FOR_DYNACONF=production`
    dotenv_path="config/.env"            # custom path for .env file to be loaded
)

settings.validators.register(
    # A name must exist in the default name
    Validator("name", must_exist=True, env="default"),
    # Custom must exist if host exists
    Validator("custom", must_exist=True, when=Validator("host", must_exist=True)),
)

settings.validators.validate()