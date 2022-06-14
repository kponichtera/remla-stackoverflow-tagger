"""
Copy data into dataset directory.
"""
import os
import shutil

from common.color_module import ColorsPrinter
from learning_service.var_names import VarNames
from learning_service.dir_util import get_directory_from_settings_or_default

DATASET_DIR = get_directory_from_settings_or_default(
    VarNames.DATASET_FOR_TRAINING_DIR,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
)
DATA_PATH = get_directory_from_settings_or_default(
    VarNames.DATA_DIR,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
)
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

if __name__=='__main__':
    copy_data()
