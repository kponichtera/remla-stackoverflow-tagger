"""
Provides a configuration management object.
"""

from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    # variables exported in .env as `REMLA_FOO=bar` becomes `settings.FOO == "bar"`
    envvar_prefix="REMLA",
    settings_files=['config/settings.yaml', 'config/.secrets.yaml'],
    # Enable layered environments
    environments=True,
    load_dotenv=True,
    # to switch environments `export DYNACONF_ENV=production`
    env_switcher="DYNACONF_ENV",
    # custom path for .env file to be loaded
    dotenv_path="config/.env"
)

settings.validators.register(
    # A name must exist in the default name
    Validator("name", must_exist=True, env="default"),
    # Custom must exist if host exists
    Validator("custom", must_exist=True,
              when=Validator("host", must_exist=True)),
)

settings.validators.validate()
