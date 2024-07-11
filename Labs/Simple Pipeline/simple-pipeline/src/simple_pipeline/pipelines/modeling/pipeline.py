
from kedro.pipeline import Pipeline, pipeline, node
from .nodes import *

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
                func=clean_dataset,
                inputs=["raw_house_prices", "params:missing_limit"],
                outputs="cleaned_house_prices",
                name="clean_dataset",
            ),
        node(
                func=feature_engineering,
                inputs=["cleaned_house_prices"],
                outputs="processed_house_prices",
                name="feature_engineering",
            ),
        node(
                func=split_dataset,
                inputs=["processed_house_prices", "params:test_size", "params:features", "params:target"],
                outputs=["train_house_prices", 'test_house_prices'],
                name="split_dataset",
            ),
        node(
                func=train_model,
                inputs=["train_house_prices", "params:features", "params:categorical_features", "params:target"],
                outputs=["model", 'coefficients'],
                name="train_model",
            ),
        node(
                func=predict_and_evaluate,
                inputs=["model", "test_house_prices", "params:target"],
                outputs="metrics",
                name="predict_and_evaluate",
            ),
    ])
