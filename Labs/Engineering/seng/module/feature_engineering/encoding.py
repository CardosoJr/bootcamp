import pandas as pd 
import numpy as np
import category_encoders as ce
from sklearn.preprocessing import LabelEncoder

class Encoding: 
    def __init__(self, convert_structure = {}):
        self.convert_structure = convert_structure

        self.methods = {'onehot' : lambda df, args: self.__onehot(df, args), 
                        'catboost' : lambda df, args: self.__catboost(df, args), 
                        'label_encoder' : lambda df, args: self.__label_encoder(df, args), 
                        'woe' : lambda df, args: self.__woe(df, args), 
        }
        self.fitted = []

    def fit(self, df: pd.DataFrame):
        self.fitted = []
        for method_name, args in self.convert_structure.items():
            if method_name not in self.methods.keys():
                raise Exception(f"Encoding method not implemented: {method_name}")
            self.methods[method_name](df, args)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for m in self.fitted:
            df = m.transform(df)
        return df

    def __onehot(self, df, args):
        m = ce.OneHot(cols = args['cols']).fit(df)
        self.fitted.append(m)

    def __woe(self, df, args) -> pd.DataFrame:
        m = ce.WOEEncoder(cols = args['cols']).fit(df, df[args['target']])
        self.fitted.append(m)

    def __catboost(self, df, args) -> pd.DataFrame:
        m = ce.CatBoostEncoder(cols = args['cols']).fit(df, df[args['target']])
        self.fitted.append(m)

    def __label_encoder(self, df, args) -> pd.DataFrame:
        mapping = []
        for c in args['cols']:
            mapping.append({'col' : c, 'mapping' : dict(zip(df[c].unique(), range(df[c].nunique())))})
        m = ce.OrdinalEncoders(cols = args['cols'], mapping = mapping).fit(df)
        self.fitted.append(m)
    
