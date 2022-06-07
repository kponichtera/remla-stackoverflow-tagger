"""
Preprocess the data to be trained by the learning algorithm.
Creates files `preprocessor.joblib` and `preprocessed_data.joblib`
"""
import os
import re
import nltk
import json
import numpy as np
import pandas as pd
from config import settings, ROOT_DIR
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from joblib import dump, load
from learning_service.src.read_data import read_data_from_file, read_unlabeled_data_from_file
nltk.download('stopwords')


REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOP_WORDS = set(stopwords.words('english'))

PREPROCESSOR_DATA_FILE_NAME = "preprocessor_data.joblib"
PREPROCESSOR_LABELS_FILE_NAME = "preprocessor_labels.joblib"

DATA_PATH = os.path.join(ROOT_DIR, settings.DATASET_FOR_TRAINING_DIR)
OUTPUT_PATH = os.path.join(ROOT_DIR, settings.OUTPUT_DIR)

np.random.seed(12321)

def text_process(text : str, stemming=False):
    """Text processor that removes bad characters and stop words.
    If needed, stemming can be performed

    Args:
        text (str): text to be processed
        stemming (bool, optional): flag to enable or disable stemming. Defaults to False.

    Returns:
        str : processed text
    """
    processed_text = text.lower()
    processed_text = re.sub(REPLACE_BY_SPACE_RE, " ", processed_text)
    processed_text = re.sub(BAD_SYMBOLS_RE, "", processed_text)
    processed_text = [word for word in processed_text.split() if not word in STOP_WORDS]
    if stemming:
        stemmed = []
        for word in processed_text:
            stemmer = SnowballStemmer('english')
            stemmed.append(stemmer.stem(word))
        processed_text = stemmed
    return " ".join(processed_text)

def create_bag_of_words_preprocessor(min_df=5, max_df=0.9):
    """Creates a bag of words preprocessor. The processor works through:
    1. Conversion of word tokens from processed title text into a bag of words
    2. Conversion of bag of words representation into TF-IDF vectorized representation
    for each title text
    3. Addition of message length

    Args:
        min_df (int, optional): TfidfVectorizer's min_df. Defaults to 5.
        max_df (float, optional): TfidfVectorizer's max_df. Defaults to 0.8.

    Returns:
        _type_: _description_
    """
    preprocessor = TfidfVectorizer(
        min_df=min_df,
        max_df=max_df,
        ngram_range = (1,2),
        token_pattern='(\S+)'
    )
    return preprocessor

def preprocess_bag_of_words(titles : pd.DataFrame, data_name='', \
    save_path=None, min_df=5, max_df=0.8, processor_prefix=""):
    """Preprocesses titles of questions into bag of words processor.

    Args:
        titles (pd.DataFrame): DataFrame of titles of StackOverflow questions
        data_name (str, optional): additional name parameter for data. Defaults to ''.
        save_path (str|None, optional): place where to save the data and preprocessor.
                                        Defaults to None.
        min_df (int, optional): TfidfVectorizer's min_df. Defaults to 5.
        max_df (float, optional): TfidfVectorizer's max_df. Defaults to 0.8.
        processor_prefix (str, optional): Prefix for processor. Defaults to "".

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    preprocessor = create_bag_of_words_preprocessor(min_df, max_df)
    preprocessed_data = preprocessor.fit_transform(titles)

    if save_path is not None and save_path != "":
        final_data_name = f'{data_name}_' if data_name != '' else ''
        final_processor_prefix = f'{processor_prefix}_' if processor_prefix != '' else ''
        dump(
            preprocessor,
            os.path.join(
                save_path,
                f'{final_processor_prefix}{PREPROCESSOR_DATA_FILE_NAME}'
            )
        )
        dump(
            preprocessed_data,
            os.path.join(
                 save_path,
                 f'{final_data_name}preprocessed_data.joblib'
            )
        )
    return preprocessed_data

def prepare_data_from_processor(titles:pd.DataFrame, save_path:str, processor_prefix=''):
    """Loads a preprocessor from a file and runs it on data.

    Args:
        titles (pd.DataFrame): DataFrame of titles of StackOverflow questions
        save_path (str): path where the preprocessor exists in

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    final_processor_prefix = f'{processor_prefix}_' if processor_prefix != '' else ''
    preprocessor = load(
        os.path.join(
            save_path,
            f'{final_processor_prefix}{PREPROCESSOR_DATA_FILE_NAME}'
        )
    )
    titles_arr = [text_process(x) for x in titles.values]
    return preprocessor.transform(titles_arr)

def prepare_labels(labels : pd.DataFrame, mlb : MultiLabelBinarizer, \
    save_path=None, labels_name=''):
    """Prepares labels for multi label classifier.

    Args:
        labels (pd.DataFrame): labels DataFrame
        save_path (str, optional): path where the preprocessor exists in. Defaults to None.
        labels_name (str, optional): _description_. Defaults to ''.

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    preprocessed_tags = mlb.fit_transform(labels.values)
    if save_path is not None and save_path != "":
        final_labels_name = f'{labels_name}_' if labels_name != '' else ''
        dump(
            preprocessed_tags,
            os.path.join(
                save_path,
                f'{final_labels_name}preprocessed_labels.joblib'
            )
        )
    return preprocessed_tags


def create_multi_label_binarizer(labels:pd.DataFrame):
    """_summary_
    """
    tags_lists = labels.values
    tags_counts = {}
    for tags in tags_lists:
        for tag in tags:
            if tag in tags_counts:
                tags_counts[tag] += 1
            else:
                tags_counts[tag] = 1
    mlb = MultiLabelBinarizer(classes=sorted(tags_counts.keys()))
    return mlb

def main():
    """Main function to run preprocessors.
    """
    train_data = read_data_from_file("train.tsv")
    validation_data = read_data_from_file("validation.tsv")
    test_data = read_unlabeled_data_from_file("test.tsv")
    print('\n################### Processed Messages ###################\n')
    with pd.option_context('expand_frame_repr', False):
        print('\n################### train_data ###################\n')
        print(train_data)
        print('\n################### validation_data ###################\n')
        print(validation_data)
        print('\n################### test_data ###################\n')
        print(test_data)
    # Create output folder
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # preprocess data
    preprocess_bag_of_words(
        train_data['title'],
        data_name="train",
        save_path=OUTPUT_PATH
    )

    val_preprocessed_data = prepare_data_from_processor(
        validation_data['title'],
        OUTPUT_PATH
    )
    dump(val_preprocessed_data, os.path.join(OUTPUT_PATH, 'val_preprocessed_data.joblib'))

    test_preprocessed_data = prepare_data_from_processor(
        test_data['title'],
        OUTPUT_PATH
    )
    dump(test_preprocessed_data, os.path.join(OUTPUT_PATH, 'test_preprocessed_data.joblib'))

    mlb = create_multi_label_binarizer(train_data['tags'])
    # preprocess labels
    prepare_labels(
        train_data['tags'],
        mlb,
        save_path=OUTPUT_PATH,
        labels_name="train"
    )
    prepare_labels(
        validation_data['tags'],
        mlb,
        OUTPUT_PATH,
        labels_name="val"
    )

    dump(mlb, os.path.join(OUTPUT_PATH, PREPROCESSOR_LABELS_FILE_NAME))

    data_preprocessor = load(
        os.path.join(
            OUTPUT_PATH,
            PREPROCESSOR_DATA_FILE_NAME
        )
    )
    vocabulary = data_preprocessor.vocabulary_
    with open(
            os.path.join(
                OUTPUT_PATH,
                'data_vocabulary.json'
            ),
            'w',
            encoding='utf-8'
        ) as outfile:
        json.dump(vocabulary, outfile, indent=2)

if __name__ == "__main__":
    main()
