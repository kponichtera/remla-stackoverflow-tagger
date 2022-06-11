import os
import pytest
import collections
import numpy as np
import pandas as pd
import unittest
from learning_service.read_data import read_data_from_file
from learning_service.text_preprocessing import text_process, preprocess_bag_of_words, \
    prepare_data_from_processor, prepare_labels, create_multi_label_binarizer
from typing import Dict, List, Union, Tuple
from parameterized import parameterized


CWD = os.path.dirname(os.path.abspath(__file__))

class PreprocessingTest(unittest.TestCase):
    """Testing model related parameters

    Args:
        unittest (unittest): testing module
    """

    def tearDown(self):
        """Tear down method when the test method finishes
        """
        files = os.listdir(CWD)
        for item in files:
            if item.endswith(".joblib"):
                os.remove(os.path.join(CWD, item))
        
    @pytest.fixture(autouse=True)
    def prepare_fixture(self):
        """Fixture to load up data
        """
        base_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            ),
            "data"
        )
        self.train_data = read_data_from_file("train.tsv", root_path=base_dir)
        self.validation_data = read_data_from_file("validation.tsv", root_path=base_dir)
        self.unordered_equality_comp = lambda x, y: collections.Counter(x) == collections.Counter(y)

    @parameterized.expand([
            [
                "SQL Server - any equivalent of Excel's CHOOSE function?",
                False,
                "sql server equivalent excels choose function"
            ],
            [
                "How to free c++ memory vector<int> * arr?",
                False,
                "free c++ memory vectorint arr"
            ],
            [
                "SQL Server - any equivalent of Excel's CHOOSE function?",
                True,
                "sql server equival excel choos function"
            ],
            [
                "How to free c++ memory vector<int> * arr?",
                True,
                "free c++ memori vectorint arr"
            ]
        ]
    )
    def test_preprocess_text(self, text_input:str, stemming:bool, text_arr_output:str) :
        """Test for preprocessing text.

        Args:
            text_input (str): text to be preprocessed
            stemming (bool): _description_
            text_arr_output (str): preprocessed string of words
        """
        output = text_process(text_input, stemming=stemming)
        self.assertEqual(output, text_arr_output)

    @parameterized.expand([
            [
                {
                    "title": ["Why odbc_exec always fail?"],
                    "tags":[['php', 'sql']]
                },
                (1,1)
            ],
            [
                {
                    "title": ["Why odbc_exec always fail?", "How to do OOP?"],
                    "tags":[['php', 'sql'], ['OOP']]
                },
                (1,1)
            ]
        ]
    )
    def test_processing_bag_of_words(
        self,
        pd_df_dict:Dict[str, List[Union[str,List[str]]]],
        shape_tuple:Tuple[int]
        ):
        """Tests processing of data through bag of words method.

        Args:
            pd_df_dict (Dict[str, List[Union[str,List[str]]]]): simulated dict data
            shape_tuple (Tuple[int]): asserted shape
        """
        data_frame = pd.DataFrame(pd_df_dict)
        processor_prefix = self.id()
        preprocessed_bag_of_words = preprocess_bag_of_words(
            data_frame[["title"]],
            min_df=1,
            max_df=1,
            processor_prefix=processor_prefix,
            data_name=processor_prefix
        )
        self.assertEqual(shape_tuple, preprocessed_bag_of_words.shape)
        files = os.listdir(CWD)
        for item in files:
            if processor_prefix in item:
                os.remove(os.path.join(CWD, item))


    @parameterized.expand([
            [
                {
                    "title": ["Why odbc_exec always fail?"],
                    "tags":[['php', 'sql']]
                }
            ],
            [
                {
                    "title": ["Why odbc_exec always fail?", "How to do OOP?"],
                    "tags":[['php', 'sql'], ['OOP']]
                }
            ]
        ]
    )
    def test_processing_bag_of_words_same_output(
        self,
        pd_df_dict:Dict[str, List[Union[str,List[str]]]]
        ):
        """Test that the saved processor outputs same results.

        Args:
            pd_df_dict (Dict[str, List[Union[str,List[str]]]]): simulated dict data
        """
        data_frame = pd.DataFrame(pd_df_dict)
        processor_prefix = self.id()
        preprocessed_bag_of_words = preprocess_bag_of_words(
            data_frame["title"],
            save_path=CWD,
            min_df=1,
            max_df=1,
            processor_prefix=processor_prefix,
            data_name=processor_prefix
        )
        preprocessed_bag_of_words_from_file = prepare_data_from_processor(
            data_frame["title"],
            CWD,
            processor_prefix=processor_prefix
        )
        self.assertEqual(preprocessed_bag_of_words.shape, preprocessed_bag_of_words_from_file.shape)

        files = os.listdir(CWD)
        for item in files:
            if processor_prefix in item:
                os.remove(os.path.join(CWD, item))

    @parameterized.expand([
        [
            {
                "tags":[['php', 'sql'], ['OOP']]
            },
            [[0, 1, 1], [1, 0, 0]]
        ],
        [
            {
                "tags":[['php', 'sql']]
            },
            [[1, 1]]
        ],
        [
            {
                "tags":[['sql']]
            },
            [[1]]
        ],
        [
            {
                "tags":[['php', 'sql'], ['OOP'], ['python']]
            },
            [[0, 1, 0, 1],[1, 0, 0, 0], [0, 0, 1, 0]]
        ]
    ])
    def test_preprocessing_labels(
        self,
        pd_df_dict:Dict[str, List[Union[str,List[str]]]],
        output:List[str]
        ):
        """Tests preprocessing of labels.

        Args:
            pd_df_dict (Dict[str, List[Union[str,List[str]]]]): dictionary for data
            output (List[str]): output answer
        """
        data_frame = pd.DataFrame(pd_df_dict)
        mlb = create_multi_label_binarizer(data_frame['tags'])
        labels = prepare_labels(data_frame['tags'], mlb)
        processed_labels = np.array(output)
        self.assertTrue(np.array_equal(processed_labels, labels))
        