"""Directory utility file for getting the right directories.
"""
import os
from src.config import settings


def get_directory_from_settings_or_default(setting : str, default: str):
    """Gets a directory either from dynaconf if it exists
    or a default fallback.

    Args:
        setting (str): dynaconf setting
        default (str): default fallback path.
    """
    settings_value = settings.get(setting.value)
    if settings_value is None:
        return default
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings_value)
    if os.path.exists(full_path):
        return full_path
    return default
