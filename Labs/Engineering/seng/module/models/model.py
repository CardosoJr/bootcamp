import git
from sklearn.base import BaseEstimator, ClassifierMixin
import pickle
from pathlib import Path

class PipelineModel(BaseEstimator, ClassifierMixin):
    def __init__(self, model, offset = 0):
        self.offset = offset
        self.model = model
        repo = git.Repo(search_parent_directories=True)
        self.commit_hash = repo.head.object.hexsha
        self.data_hash = {}

    def __eq__(self, other):
        return self.offset == other.offset

    def set_data_hash(self, hash):
         self.data_hash = hash

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train) 
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def save(self, path):
        pickle.dump(self, Path(path).open(mode = 'wb'))

    @classmethod
    def load(cls, path):
        return pickle.load(Path(path).open(mode = 'rb'))