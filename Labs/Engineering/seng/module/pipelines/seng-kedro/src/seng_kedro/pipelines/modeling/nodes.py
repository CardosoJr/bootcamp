import pandas as pd
import numpy as np 

from module.models.factory import ModelFactory
from module.models.development import training, predict
from module.reporting.model_analysis import ModelAnalysis
import module.feature_engineering.encoding as enc
import module.data.split as split

def training_node(params, data, raw_hash):
    y = data.pop('target')
    model = training(data, y, params)
    model.set_data_hash(raw_hash)
    return model

def predict_node(model, data):
    pred = predict(data.loc[:, data.columns != "target"], model)
    data['predictions'] = pred
    return data

def metrics_node(*data):
    concat_data = pd.concat(data)
    report = ModelAnalysis(concat_data)
    return report.metrics()


def split_dataset(df_o: pd.DataFrame, params):
    train_data = []
    val_data = []
    if params['method'] == 'kfold':
        splitter = split.KFoldSplit(seed = 42, num_folds = params['params']['num_split'])
        idx = splitter.fit_transform(df_o)

        for idx_train, idx_test in idx:
            train_data.append(df_o.loc[idx_train])
            val_data.append(df_o.loc[idx_test])
    else:
        splitter = split.Split(seed = 42, validation_size = None, test_size = params['params']['test_size'])
        idx_train, idx_validation, idx_test = splitter.fit_transform(df_o)
        train_data.append(df_o.loc[idx_train])
        val_data.append(df_o.loc[idx_test])

    return tuple(train_data + val_data)

def encode(df_train: pd.DataFrame, df_val: pd.DataFrame, params):
    convert_structure = {}
    for method, cols in params['pre_processing'].items():
        convert_structure[method] = {'cols' : cols, 'target' : 'target'}
    encoder = enc.Encoding(convert_structure = convert_structure)

    encoder.fit(df_train)
    df_train = encoder.transform(df_train)
    df_val = encoder.transform(df_val)

    return df_train, df_val