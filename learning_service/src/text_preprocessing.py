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
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_union, make_pipeline
from joblib import dump, load
from read_data import read_data_from_file

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOP_WORDS = set(stopwords.words('english'))
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

def create_bag_of_words_preprocessor(save_path):
    """Creates a bag of words preprocessor. The processor works through:
    1. Conversion of word tokens from processed title text into a bag of words
    2. Conversion of bag of words representation into tfidf vectorized representation for each title text
    3. Addition of message length

    Args:
        save_path str: save path for words preprocessor. If None or empty string,
                        no saving is perfomed.
    """
    preprocessor = make_union(
        make_pipeline(
            CountVectorizer(analyzer=text_process),
            TfidfTransformer()
        ),
        FunctionTransformer(extract_processed_text_len, validate=False)
    )
    if save_path is not None and save_path != "":
        dump(preprocessor, f'{save_path}/preprocessor_bag_of_words.joblib')
    return preprocessor

def preprocess_bag_of_words(titles:pd.DataFrame, data_name:str, save_path=None):
    """Preprocesses titles of questions into bag of words processor.

    Args:
        titles (pd.DataFrame): DataFrame of titles of StackOverflow questions
        save_path (str|None, optional): place where to save the data and preprocessor.
                                        Defaults to None.

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    preprocessor = create_bag_of_words_preprocessor(save_path)
    preprocessed_data = preprocessor.fit_transform(titles)

    if save_path is not None and save_path != "":
        dump(preprocessed_data, f'{save_path}/preprocessed_{data_name}_data.joblib')
    return preprocessed_data

def prepare_from_processor(titles:pd.DataFrame, save_path:str):
    """Loads a preprocessor from a file and runs it on data.

    Args:
        titles (pd.DataFrame): DataFrame of titles of StackOverflow questions
        save_path (str): save path for the preprocessor

    Returns:
        ndarray[float64] | Any | ndarray: processed data
    """
    preprocessor = load(f'{save_path}/preprocessor_bag_of_words.joblib')
    return preprocessor.transform(titles)


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
