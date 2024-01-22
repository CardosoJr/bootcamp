from .factory import ModelFactory
import git

def training(X_train, y, params): 
    factory = ModelFactory()
    model = factory.build_model(params)
    model.fit(X_train, y)
    return model

def predict(X_test, model):
    pred = model.predict_proba(X_test)[:,1]
    return pred 