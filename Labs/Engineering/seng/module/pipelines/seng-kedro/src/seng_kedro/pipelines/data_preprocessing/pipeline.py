from kedro.pipeline import Pipeline, node, pipeline
from .nodes import *

from pathlib import Path

def create_pipeline(**kwargs) -> Pipeline:
    catalog = kwargs['catalog']
    params = catalog.datasets.parameters.load()

    processing_pipeline =  pipeline([
        node(
                func=get_raw_hash,
                inputs=["olist_orders_dataset", 
                        "olist_order_items_dataset", 
                        "olist_customers_dataset",
                        "olist_order_reviews_dataset", 
                        "olist_order_payments_dataset",
                        "olist_geolocation_dataset",
                        "olist_products_dataset",
                        "olist_sellers_dataset",
                        ],
                outputs=["raw_hash_tracking", 'raw_hash'],
                name="get_raw_data_hash",
            ),

        node(
                func=prepare_and_merge,
                inputs=["olist_orders_dataset", 
                        "olist_order_items_dataset", 
                        "olist_customers_dataset",
                        "olist_order_reviews_dataset", 
                        "olist_order_payments_dataset",
                        "olist_geolocation_dataset",
                        "olist_products_dataset",
                        "olist_sellers_dataset",
                        ],
                outputs=["processed_order_items", 'processed_orders'],
                name="prepare_and_merge",
            ),

        node(
                func=order_items_engineering,
                inputs="processed_order_items", 
                outputs="fe_order_items",
                name="order_items_engineering",
            ),

        node(
                func=orders_engineering,
                inputs="processed_orders", 
                outputs="fe_orders",
                name="orders_engineering",
            ),

        node(
                func=create_finaldataset,
                inputs=["fe_orders", "fe_order_items", "params:features"], 
                outputs="final_dataset",
                name="create_finaldataset",
            ),
    ])

    if 'split' in params.keys():
        num_splits = params['split']['params']['num_split']
        nodes = [
            node(
                func = split_dataset,
                inputs = ["final_dataset", "params:split"],
                outputs = [f"df_train_{i}" for i in range(num_splits)] + [f"df_val_{i}" for i in range(num_splits)],
                name = "splitting_datasets"
            ),            
        ]

        for i in range(num_splits):
            n = node(
                func = encode,
                inputs = [f"df_train_{i}", f"df_val_{i}", "params:features"],
                outputs = [f"df_train_final_{i}", f"df_val_final_{i}"],
                name = f"encoding_{i}" 
            )
            nodes.append(n)

        encoding_pipeline = pipeline(nodes)

        return processing_pipeline + encoding_pipeline
    else:
        return processing_pipeline