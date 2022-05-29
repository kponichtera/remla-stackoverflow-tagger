"""
Preprocess the data to be trained by the learning algorithm.
Creates files `preprocessor.joblib` and `preprocessed_data.joblib`
"""
import os
import re
import nltk
import string
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
nltk.download('stopwords')
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_union, make_pipeline
from joblib import dump, load

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOP_WORDS = set(stopwords.words('english'))
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")

def load_data(filename: str, sep='\t'):
    """Loads data from a file.

    Args:
        filename (str): name of a file to be loaded.
        sep (str, optional): delimiter for file. Defaults to '\t'.

    Returns:
        pd.DataFrame: pandas' DataFrame
    """
    messages = pd.read_csv(
        os.path.join(DATA_PATH, filename),
        sep=sep
    )
    return messages

def text_process(text : str, stemming=False):
    """Text processor that removes bad characters and stop words.
    If needed, stemming can be performed

    Args:
        text (str): text to be processed
        stemming (bool, optional): flag to enable or disable stemming. Defaults to False.

    Returns:
        list[str]: processed text into a list of strings
    """
    processed_text = text.lower()
    processed_text = re.sub(REPLACE_BY_SPACE_RE, " ", processed_text)
    processed_text = re.sub(BAD_SYMBOLS_RE, "", processed_text)
    processed_text = [word for word in processed_text.split() if not word in STOP_WORDS]
    if stemming:
        stemmed = ''
        for word in processed_text:
            stemmer = SnowballStemmer('english')
            stemmed.join(stemmer.stem(word) + ' ')
        processed_text = stemmed.split()
    return processed_text

def extract_processed_text_len(data: list[str]):
    """A extractor of lengths for list of words and
    reshapes it with numpy so that it works with `make_union`.

    e.g.
    >>> extract_processed_text_len(['word', 'que', 'as'])
    [[4]
     [3]
     [2]]

    Args:
        data (list[str]): list of words

    Returns:
        np.array: numpy array for `make_union` to process
    """
    return np.array([len(item) for item in data]).reshape(-1, 1)

def _preprocess(messages):
    '''
    1. Convert word tokens from processed msgs dataframe into a bag of words
    2. Convert bag of words representation into tfidf vectorized representation for each message
    3. Add message length
    '''
    preprocessor = make_union(
        make_pipeline(
            CountVectorizer(analyzer=text_process),
            TfidfTransformer()
        ),
        # append the message length feature to the vector
        FunctionTransformer(extract_processed_text_len, validate=False)
    )

    preprocessed_data = preprocessor.fit_transform(messages['message'])
    dump(preprocessor, 'output/preprocessor.joblib')
    dump(preprocessed_data, 'output/preprocessed_data.joblib')
    return preprocessed_data

def prepare(message):
    preprocessor = load('output/preprocessor.joblib')
    return preprocessor.transform([message])


def main():
    messages = load_data()
    print('\n################### Processed Messages ###################\n')
    with pd.option_context('expand_frame_repr', False):
        print(messages)
    _preprocess(messages)

if __name__ == "__main__":
    main()
