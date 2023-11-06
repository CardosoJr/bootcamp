from kedro.pipeline import Pipeline, node, pipeline
from .nodes import *

from pathlib import Path

def create_pipeline(**kwargs) -> Pipeline:
    catalog = kwargs['catalog']
    params = catalog.datasets.parameters.load()

    processing_pipeline =  pipeline([
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
        return processing_pipeline
    else:
        return processing_pipeline