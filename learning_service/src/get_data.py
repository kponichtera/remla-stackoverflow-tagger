"""
Copy data into dataset directory.
"""
import os
import shutil
from var_names import VarNames
from dir_util import get_directory_from_settings_or_default

setting_dir = VarNames.DATASET_FOR_TRAINING_DIR
DATASET_DIR = get_directory_from_settings_or_default(
    setting_dir,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
)
settings_value = VarNames.DATA_DIR
DATA_PATH = get_directory_from_settings_or_default(
    setting_dir,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
)

def copy_data():
    """
    Copies data from `data/` folder and creates
    a `dataset/` folder which dvc will read from.
    """
    if not os.path.exists(DATASET_DIR):
        os.mkdir(DATASET_DIR)
    shutil.copytree(DATA_PATH, DATASET_DIR, dirs_exist_ok=True)

if __name__=='__main__':
    copy_data()
