from kedro.pipeline import Pipeline, node, pipeline
from ..modeling import nodes as mod_nodes

def create_pipeline(**kwargs) -> Pipeline:
    catalog = kwargs['catalog']
    params = catalog.datasets.parameters.load()


    nodes = [
            node(
                func = mod_nodes.split_dataset,
                inputs = ["final_dataset", "params:prod_split"],
                outputs = ["df_train_prod", "df_test_prod"],
                name = "prod_splitting"
            ),            
            node(
                func = mod_nodes.encode,
                inputs = [f"df_train_prod", f"df_test_prod", "params:features"],
                outputs = [f"df_train_final_prod", f"df_test_final_prod"],
                name = f"prod_encoding" 
            ),
            node(
                func = mod_nodes.training_node,
                inputs = ["params:model", f"df_train_final_prod", 'raw_hash'],
                outputs = f"model_prod",
                name = f"prod_training"
            ),      
            node(
                func = mod_nodes.predict_node,
                inputs = [f"model_prod", f"df_test_final_prod"],
                outputs = f"df_test_pred",
                name = f"prod_predict"
            ),  
            node(
                func = mod_nodes.metrics_node,
                inputs = [f"df_test_pred"],
                outputs = f"metrics_prod",
                name = "prod_evaluate"
            ),     
        ]
    
    pipe = pipeline(nodes)

    return pipe