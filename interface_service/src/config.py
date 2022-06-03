"""
Provides a configuration management object.
"""

from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    # variables exported in .env as `REMLA_FOO=bar` becomes `settings.FOO == "bar"`
    envvar_prefix="REMLA",
    environments=False,
    load_dotenv=False
)
