"""
File that presents and shows information about data and statistics about it.
"""
import os
from ast import literal_eval
import pandas as pd
import tensorflow_data_validation as tfdv
from termgraph import termgraph as tg

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")

TRAIN_DATA_FILE = 'train.tsv'
VALIDATION_DATA_FILE = 'validation.tsv'
TEST_DATA_FILE = 'test.tsv'
MAIN_COLOR = 94

def read_labeled_data(filename: str, sep='\t') :
    """Reads labeled data from a file.

    Args:
        filename (str): File to be read from.
        sep (str, optional): File separator. Defaults to '\t'.
    
    Returns:
        pd.DataFrame: DataFrame generated from the labeled data file
    """
    data = read_data_from_file(filename, sep=sep)
    data['tags'] = data['tags'].apply(literal_eval)
    return data

def read_data_from_file(filename: str, sep='\t', root_path=DATA_PATH):
    """Loads data from a file.

    Args:
        filename (str): name of a file to be loaded.
        sep (str, optional): delimiter for file. Defaults to '\t'.
        root_path (_type_, optional): root path where the file should be found. Defaults to DATA_PATH.

    Returns:
        pd.DataFrame: pandas' DataFrame of StackOverflow's titles and tags
    """  
    data = pd.read_csv(
        os.path.join(root_path, filename),
        sep=sep,
        dtype={'title': 'str', 'tags': 'str'}
    )
    data = data[["title", "tags"]]
    return data

def display_data_schema(filename: str):
    """Display schema information for a given data file.

    Args:
        filename (str): File name of which to display the schema
    """
    print("\n\n")
    full_file_path = os.path.join(DATA_PATH, filename)
    stats_options = tfdv.StatsOptions(enable_semantic_domain_stats=True)
    stats = tfdv.generate_statistics_from_csv(
        full_file_path,
        delimiter='\t',
        stats_options=stats_options
    )
    schema = tfdv.infer_schema(stats)
    print("\n\n",f"\033[{MAIN_COLOR}m------------ Schema: {filename} --------------\033[0m\n")
    tfdv.display_schema(schema)
    print("\n\n")

def display_data_information():
    """Displays information about data.
    """
    train = read_labeled_data(TRAIN_DATA_FILE)
    print(f'\033[{MAIN_COLOR}m',
          "\n++++++++++++++++++++++Train Data++++++++++++++++++++++\033[0m\n",
          train.head().to_markdown(),
          '\n'
    )
    display_data_schema(TRAIN_DATA_FILE)
    
    validation = read_labeled_data(VALIDATION_DATA_FILE)
    print(
        f'\033[{MAIN_COLOR}m',
        "\n++++++++++++++++++++++Validation Data++++++++++++++++++++++\033[0m\n",
        validation.head().to_markdown(),
        '\n'
    )
    display_data_schema(VALIDATION_DATA_FILE)
    
    test = read_data_from_file(TEST_DATA_FILE)
    print(
        f'\033[{MAIN_COLOR}m',
        "\n++++++++++++++++++++++Test Data++++++++++++++++++++++\033[0m\n",
        test.head().to_markdown(),
        '\n'
    )
    display_data_schema(TEST_DATA_FILE)
    
    tags_counts = {}
    y_train = train['tags'].values
    for tags in y_train:
        for tag in tags:
            if tag in tags_counts:
                tags_counts[tag] += 1
            else:
                tags_counts[tag] = 1
    print(
        f'\033[{MAIN_COLOR}m',
        "\n++++++++++++++++++++++Tags statistics++++++++++++++++++++++\033[0m\n",
    )
    most_frequent_tags = sorted(tags_counts.items(), key=lambda x: x[1], reverse=True)
    print(f"No. of tags : {len(tags_counts)}")
    print(f"\033[{MAIN_COLOR}m----------------- 10 Most frequent tags\033[0m\n")
    labels = [item[0] for item in most_frequent_tags[:10]]
    data = [[item[1]] for item in most_frequent_tags[:10]]
    bar_width = 75
    bar_lengths = [[item[0] / data[0][0] * bar_width] for item in data]
    args = {'title': "", 'width': bar_width, 'format': '{:d}',
            'suffix': '', 'no_labels': False,
        'color': None, 'vertical': False, 'stacked': True,
        'different_scale': False, 'calendar': False,
        'start_dt': None, 'custom_tick': '', 'delim': '',
        'verbose': False, 'version': False}
    colors = [MAIN_COLOR]
    tg.stacked_graph(labels, data, bar_lengths, 1, args, colors)

if __name__=='__main__':
    display_data_information()
