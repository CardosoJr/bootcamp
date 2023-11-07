import pandas as pd 
import numpy as np 
from abc import ABC, abstractmethod

class Problem(ABC):
    def __init__(self, target):
        self.target = target
    @abstractmethod
    def get_data(self):
        pass
    @abstractmethod
    def get_target(self):
        pass

class BinaryClassProblem(Problem):
    def __init__(self, target, data):
        super().__init__(target = target)
        self.data = data
        data['target'] = np.where(data['review_score'] < 5, 0, 1)
        data.drop(columns = ['review_score'], inplace = True)
        # self.target = self.data.pop('target')
    def get_data(self):
        return self.data
    def get_target(self):
        return self.data['target']#self.target

class MultClassProblem(Problem):
    def __init__(self, target, data):
        super().__init__(target = target)
        self.data = data
        data['target'] = data['review_score'].round(0).astype(int)
        data.drop(columns = ['review_score'], inplace = True)
        # self.target = self.data.pop('target')
    def get_data(self):
        return self.data
    def get_target(self):
        return self.data['target'] #self.target