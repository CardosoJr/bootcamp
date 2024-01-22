import pandas as pd
import numpy as np 

from module.models.factory import ModelFactory
from module.models.development import training, predict
from module.reporting.model_analysis import ModelAnalysis

def training_node(params, data):
    y = data.pop('target')
    model = training(data, y, params)
    return model

def predict_node(model, data):
    pred = predict(data.loc[:, data.columns != "target"], model)
    data['predictions'] = pred
    return data

def metrics_node(*data):
    concat_data = pd.concat(data)
    report = ModelAnalysis(concat_data)
    return report.metrics()