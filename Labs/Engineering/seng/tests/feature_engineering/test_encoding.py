from pathlib import Path
import pandas as pd
import numpy as np

# @pytest.fixture
# def df_train():
#     np.random.seed(42)
#     df_train = pd.DataFrame({"cat_col" : np.random.choice(['a', 'b', 'c'], 100), 'target' : (np.random.uniform(size = 100) > 0.7) * 1})
#     return df_train

def test_encoding():
    np.random.seed(42)
    df_train = pd.DataFrame({"cat_col" : np.random.choice(['a', 'b', 'c'], 10), 'target' : (np.random.uniform(size = 10) > 0.7) * 1})
    from src.feature_engineering import encoding 
    params = {'catboost' : {'cols' : ['cat_col'], 'target' : 'target'}}
    enc = encoding.Encoding(params)   
    enc.fit(df_train)
    df_enc = enc.transform(df_train)
    assert (df_enc['cat_col'].round(2).values == [0.34, 0.6 , 0.34, 0.34, 0.6 , 0.6 , 0.34, 0.4 , 0.34, 0.34]).sum() == 10