from pathlib import Path
import pandas as pd
import numpy as np
from tests.test_sample import sample_data

def test_encoding(sample_data):
    assert sample_data['a'].mean() == 2
    # np.random.seed(42)
    # df_train = pd.DataFrame({"cat_col" : np.random.choice(['a', 'b', 'c'], 10), 'target' : (np.random.uniform(size = 10) > 0.7) * 1})
    # from module.feature_engineering import encoding 
    # params = {'catboost' : {'cols' : ['cat_col'], 'target' : 'target'}}
    # enc = encoding.Encoding(params)   
    # enc.fit(df_train)
    # df_enc = enc.transform(df_train)
    # assert (df_enc['cat_col'].round(2).values == [0.34, 0.6 , 0.34, 0.34, 0.6 , 0.6 , 0.34, 0.4 , 0.34, 0.34]).sum() == 10