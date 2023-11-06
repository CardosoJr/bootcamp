import pandas as pd 
import numpy as np
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

class Split(ABC): 
    @abstractmethod
    def fit_transform(self, data):
        pass

class SimpleSplit(Split):
    def __init__(self, test_size = 0.15, validation_size = 0.3):
        self.test_size = test_size
        self.validation_size = validation_size

    def fit_transform(self, data):
        train, test = train_test_split(data.index, test_size = self.test_size)
        validation = []
        if self.validation_size:
            train, validation = train_test_split(data[train].index, test_size = self.validation_size, )
        return train, validation, test

class KFoldSplit(Split):
    def __init(self, num_folds):
        self.num_folds = num_folds

    def fit_transform(self, data):
        kf = KFold(n_splits=self.num_fold, shuffle = True, random_state = seed)
        folds = [(id_train, id_test) in kf.split(data)]
        return folds
        
class Backtester(Split):
    def fit_transform(self, data):
        pass