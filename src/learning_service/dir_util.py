"""Directory utility file for getting the right directories.
"""
import os
from enum import Enum

from learning_service.config import settings


def get_directory_from_settings_or_default(setting: Enum, default: str):
    """Gets a directory either from dynaconf if it exists
    or a default fallback.

    Args:
        setting (Enum): dynaconf setting
        default (str): default fallback path.
    """
    settings_value = settings.get(setting.value)
    if os.path.exists(settings_value):
        return settings_value
    if settings_value is None:
        return default
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings_value)
    if os.path.exists(full_path):
        return full_path
    return default
