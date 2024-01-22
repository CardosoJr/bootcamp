import git
from sklearn.base import BaseEstimator, ClassifierMixin

class PipelineModel(BaseEstimator, ClassifierMixin):
    def __init__(self, model):
        self.model = model
        repo = git.Repo(search_parent_directories=True)
        self.commit_hash = repo.head.object.hexsha
    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train) 
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)