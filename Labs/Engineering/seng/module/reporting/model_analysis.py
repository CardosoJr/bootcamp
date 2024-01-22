from abc import ABC, abstractmethod
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

class ModelAnalysis():
    def __init__(self, df, pred_column = 'predictions', target_column = 'target', threshold = 0.5):
        self.df = df
        self.target_column = target_column
        self.threshold = threshold
        self.pred_column = pred_column

    def metrics(self):
        return { 'accuracy' : accuracy_score(self.df[self.target_column], self.df[self.pred_column] >= self.threshold), 
                 'f1_score' : f1_score(self.df[self.target_column], self.df[self.pred_column] >= self.threshold), 
                 'roc_auc' : roc_auc_score(self.df[self.target_column], self.df[self.pred_column]), 
        }
    
    def diagnose(self):
        """
            TODO: 
                - Feature Importance
                - Local errors
        """
        raise Exception("Not implemented")

class MultiClassModelAnalysis(ModelAnalysis):
    def __init__(self):
        raise Exception("Not implemented")
