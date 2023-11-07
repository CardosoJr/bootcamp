from pathlib import Path

import pytest

import pandas as pd
import numpy as np

@pytest.fixture
def define_root_dir():
    from pathlib import Path
    import sys
    parent_dir = Path("../../../")
    sys.path.append(str(parent_dir))

def test_encoding():
    define_root_dir()
    from src.seng_kedro.pipelines.data_preprocessing.nodes import encode
    np.random.seed(42)
    df_train = pd.DataFrame({"cat_col" : np.random.choice(['a', 'b', 'c'], 100), 'target' : (np.random.uniform(size = 100) > 0.7) * 1})
    params = {'catboost' : {'cols' : ['cat_col'], 'target' : 'target'}}
    df1, df2 = encode(df_train, df_train, params)
    assert df1.equals(df_train)