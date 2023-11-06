import pandas as pd 
import numpy as np

def train_model(model_builder, args, X_train, y_train):
    model = model_builder(**args)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, metric):
    y_pred = model.predict(X_test)
    return metric(y_test, y_pred)