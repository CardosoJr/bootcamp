from kedro.pipeline import Pipeline, node, pipeline
from .nodes import *

def create_pipeline(**kwargs) -> Pipeline:
    catalog = kwargs['catalog']
    params = catalog.datasets.parameters.load()

    if 'split' in params.keys():
        num_splits = params['split']['params']['num_split']
        nodes = []
        for i in range(num_splits):
            nodes.extend(
                [
                    node(
                        func = training_node,
                        inputs = ["params:model", f"df_train_final_{i}"],
                        outputs = [f"model_{i}"],
                        name = f"training_{i}"
                    ),      
                    node(
                        func = predict_node,
                        inputs = [f"model_{i}", f"df_val_final_{i}"],
                        outputs = [f"df_val_pred_{i}"],
                        name = f"predict_{i}"
                    ),  
                ]   
            )      
        
        nodes.append(
            node(
                func = metrics_node,
                inputs = [f"df_val_pred_{i}" for i in range(num_splits)],
                outputs = [f"metrics"],
                name = "evaluate"
            ),     
        )

    pipe = pipeline(nodes)

    return pipe
