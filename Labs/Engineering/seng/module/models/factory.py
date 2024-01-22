from abc import ABC, abstractmethod
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from .model import PipelineModel

class FactoryInterface(ABC):
    @abstractmethod
    def build_model(self, params):
        pass

class ModelFactory(FactoryInterface):

    model_dict = {
        "xgboost" : lambda hyperparameters: XGBClassifier(**hyperparameters),
        "catboost" : lambda hyperparameters: CatBoostClassifier(**hyperparameters),
        "lgbm" : lambda hyperparameters: LGBMClassifier(**hyperparameters),
    }

    def build_model(self, params):
        if params['type'] not in self.model_dict.keys():
            raise Exception(f"Model {params['type']} not implemented. Available models are {', '.join(self.model_dict.keys())}")
        return PipelineModel(self.model_dict[params["type"]](params["hyperparameters"]))     

    def __build_ensemble(self, params):
        raise Exception("Not Implemented")   
