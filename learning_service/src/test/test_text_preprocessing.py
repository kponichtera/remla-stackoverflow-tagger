import os
import pytest
import unittest
import collections
import numpy as np
from typing import List
from parameterized import parameterized
from ..text_preprocessing import text_process, extract_processed_text_len
from ..read_data import read_data_from_file




class PreprocessingTest(unittest.TestCase):
    """Testing model related parameters"""
    
    @pytest.fixture(autouse=True)
    def prepare_fixture(self):
        """Fixture to load up data"""
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
                ["sql","server","equivalent","excels","choose","function"]
            ],
            [
                "How to free c++ memory vector<int> * arr?",
                False,
                ["free","c++","memory","vectorint","arr"]
            ],
            [
                "SQL Server - any equivalent of Excel's CHOOSE function?",
                True,
                ['sql', 'server', 'equival', 'excel', 'choos', 'function']
            ],
            [
                "How to free c++ memory vector<int> * arr?",
                True,
                ['free', 'c++', 'memori', 'vectorint', 'arr']
            ]
        ]
    )
    def test_preprocess_text(self, text_input:str, stemming:bool, text_arr_output:List[str]) :
        """Test for preprocessing text.

        Args:
            text_input (str): text to be preprocessed
            stemming (bool): _description_
            text_arr_output (List[str]): preprocessed array of words
        """
        output = text_process(text_input, stemming=stemming)
        self.assertTrue(self.unordered_equality_comp(output, text_arr_output))

    @parameterized.expand([
            [
                ["sql","server","equivalent","excels","choose","function"],
                [[3], [6], [10], [6], [6], [8]]
            ],
            [
                ["free","c++","memory","vectorint","arr"],
                [[4], [3], [6], [9], [3]]
            ],
            [
                ['sql', 'server', 'equival', 'excel', 'choos', 'function'],
                [[3], [6], [7], [5], [5], [8]]
            ],
            [
                ['free', 'c++', 'memori', 'vectorint', 'arr'],
                [[4], [3], [6], [9], [3]]
            ]
        ]
    )
    def test_processed_text_len(self, text_arr_input:List[str], text_len_arr_output:List[int]) :
        """Test to check that right lengths array is output.

        Args:
            text_arr_input (List[str]): text array
            text_len_arr_output (List[int]): lengths array of text
        """
        output = extract_processed_text_len(text_arr_input)
        self.assertTrue(np.array_equal(output, np.array(text_len_arr_output)))
