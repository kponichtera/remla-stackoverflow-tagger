"""
Preprocess the data to be trained by the learning algorithm.
Creates files `preprocessor.joblib` and `preprocessed_data.joblib`
"""
import os
import re
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from typing import List
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_union
from joblib import dump, load
from learning_service.src.read_data import read_data_from_file

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOP_WORDS = set(stopwords.words('english'))
PREPROCESSOR_FILE_NAME = "preprocessor_bag_of_words.joblib"
PREPROCESSOR_LABELS_FILE_NAME = "preprocessor_labels.joblib"
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
np.random.seed(12321)

def text_process(text : str, stemming=False):
    """Text processor that removes bad characters and stop words.
    If needed, stemming can be performed

    Args:
        text (str): text to be processed
        stemming (bool, optional): flag to enable or disable stemming. Defaults to False.

    Returns:
        List[str]: processed text into a list of strings
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
    return processed_text

def extract_processed_text_len(data: List[str]):
    """A extractor of lengths for list of words and
    reshapes it with numpy so that it works with `make_union`.

    e.g.
    >>> extract_processed_text_len(['word', 'que', 'as'])
    [[4]
     [3]
     [2]]

    Args:
        data (List[str]): list of words

    Returns:
        np.array: numpy array for `make_union` to process
    """
    return np.array([len(item) for item in data]).reshape(-1, 1)

def create_bag_of_words_preprocessor(min_df=5, max_df=0.8):
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
    preprocessor = make_union(
        TfidfVectorizer(
            min_df=min_df,
            max_df=max_df,
            sublinear_tf=True,
            ngram_range = (1,2),
            token_pattern='(\S+)',
            use_idf=True
        ),
        FunctionTransformer(extract_processed_text_len, validate=False)
    )
    return preprocessor

def preprocess_bag_of_words(titles:pd.DataFrame, data_name='', save_path=None, min_df=5, max_df=0.8):
    """Preprocesses titles of questions into bag of words processor.

    Args:
        titles (pd.DataFrame): DataFrame of titles of StackOverflow questions
        data_name (str, optional): _description_. Defaults to ''.
        save_path (str|None, optional): place where to save the data and preprocessor.
                                        Defaults to None.
        min_df (int, optional): TfidfVectorizer's min_df. Defaults to 5.
        max_df (float, optional): TfidfVectorizer's max_df. Defaults to 0.8.

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    preprocessor = create_bag_of_words_preprocessor(min_df, max_df)
    preprocessed_data = preprocessor.fit_transform([item[0] for item in titles.values])

    if save_path is not None and save_path != "":
        final_data_name = f'{data_name}_' if data_name != '' else ''
        dump(preprocessor, os.path.join(save_path, PREPROCESSOR_FILE_NAME))
        dump(preprocessed_data, os.path.join(save_path, f'preprocessed_{final_data_name}data.joblib'))
    return preprocessed_data

def prepare_from_processor(titles:pd.DataFrame, save_path:str):
    """Loads a preprocessor from a file and runs it on data.

    Args:
        titles (pd.DataFrame): DataFrame of titles of StackOverflow questions
        save_path (str): path where the preprocessor exists in

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    preprocessor = load(os.path.join(save_path,PREPROCESSOR_FILE_NAME))
    return preprocessor.transform([item[0] for item in titles.values])

def prepare_labels(labels:pd.DataFrame, save_path=None):
    """Prepares labels for multi label classifier.

    Args:
        labels (pd.DataFrame): labels DataFrame
        save_path (str, optional): path where the preprocessor exists in. Defaults to None.

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    tags_lists = [item[0] for item in labels.values]
    tags_counts = {}
    for tags in tags_lists:
        for tag in tags:
            if tag in tags_counts:
                tags_counts[tag] += 1
            else:
                tags_counts[tag] = 1
    mlb = MultiLabelBinarizer(classes=sorted(tags_counts.keys()))
    preprocessed_tags = mlb.fit_transform(tags_lists)
    if save_path is not None and save_path != "":
        dump(mlb, os.path.join(save_path, PREPROCESSOR_LABELS_FILE_NAME))
        dump(preprocessed_tags, os.path.join(save_path, 'preprocessed_preprocessed_tags.joblib'))
    return preprocessed_tags

def main():
    """Main function to run preprocessors.
    """
    train_data = read_data_from_file("train.tsv")
    validation_data = read_data_from_file("validation.tsv")
    print('\n################### Processed Messages ###################\n')
    with pd.option_context('expand_frame_repr', False):
        print('\n################### train_data ###################\n')
        print(train_data)
        print('\n################### validation_data ###################\n')
        print(validation_data)

if __name__ == "__main__":
    main()
