"""
Copy data into dataset directory.
"""
import os
import shutil

from common.color_module import ColorsPrinter
from learning_service.config import settings, VarNames

DATASET_DIR = settings[VarNames.DATASET_FOR_TRAINING_DIR.value]
DATA_PATH = settings[VarNames.DATA_DIR.value]
RESOURCES_DATA_PATH = "learning_service/data"


def copy_data():
    """
    Copies data from `data/` folder and creates
    a `dataset/` folder which dvc will read from.
    """
    if not os.path.exists(DATASET_DIR):
        ColorsPrinter.log_print_info(f'Directory {DATASET_DIR} does not exist - creating')
        os.mkdir(DATASET_DIR)
    shutil.copytree(DATA_PATH, DATASET_DIR, dirs_exist_ok=True)


def copy_data_from_resources():
    """
    Copies data from application resources folder and creates
    a `dataset/` folder which dvc will read from.
    """
    if not os.path.exists(DATASET_DIR):
        ColorsPrinter.log_print_info(f'Directory {DATASET_DIR} does not exist - creating')
        os.mkdir(DATASET_DIR)
    shutil.copytree(RESOURCES_DATA_PATH, DATASET_DIR, dirs_exist_ok=True)


if __name__ == '__main__':
    copy_data()
