"""
Copy data into dataset directory.
"""
import os
import shutil
from config import settings, ROOT_DIR

DATASET_DIR = os.path.join(ROOT_DIR, settings.DATASET_FOR_TRAINING_DIR)
DATA_PATH = os.path.join(ROOT_DIR, settings.DATA_DIR)

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
