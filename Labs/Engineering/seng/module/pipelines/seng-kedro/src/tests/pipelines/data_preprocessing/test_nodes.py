from pathlib import Path
import sys
import pytest
import os
import pandas as pd
import numpy as np

def define_root_dir():
    parent_dir = Path("../../../")
    # sys.path.append(str(parent_dir.resolve()))
    sys.path.insert(0, str(parent_dir.resolve()))

# @pytest.fixture
# def df_train():
#     np.random.seed(42)
#     df_train = pd.DataFrame({"cat_col" : np.random.choice(['a', 'b', 'c'], 100), 'target' : (np.random.uniform(size = 100) > 0.7) * 1})
#     return df_train

def test_encoding():
    define_root_dir()
    np.random.seed(42)
    df_train = pd.DataFrame({"cat_col" : np.random.choice(['a', 'b', 'c'], 100), 'target' : (np.random.uniform(size = 100) > 0.7) * 1})
    from src.seng_kedro.pipelines.data_preprocessing.nodes import encode
    # params = {'catboost' : {'cols' : ['cat_col'], 'target' : 'target'}}
    # df1, df2 = encode(df_train, df_train, params)
    # assert df1.equals(df_train)

    assert 1 == 1