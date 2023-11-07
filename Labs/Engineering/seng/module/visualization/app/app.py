import streamlit as st
import pandas as pd 
import numpy as np 
from pathlib import Path
pd.set_option('display.max_columns', 500)
import warnings
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('darkgrid')
# sns.set_context('talk')
sns.set_palette('rainbow')
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

import os
os.chdir(str(Path("../../../")))
print(os.chdir)

import module.data.preprocessing as pp
import module.data.problem_definition as problem
import module.data.split as split
import module.feature_engineering.engineering as eng
import module.feature_engineering.encoding as enc
import module.models.train_model as train

file_path = "./data/raw/"
df_o = pd.read_parquet(Path(file_path + 'olist_orders_dataset.pq'))
for c in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',	'order_delivered_customer_date', 'order_estimated_delivery_date']:
    df_o[c] = pd.to_datetime(df_o[c])
df_oi = pd.read_parquet(Path(file_path + 'olist_order_items_dataset.pq'))
for c in ['shipping_limit_date']:
    df_oi[c] = pd.to_datetime(df_oi[c])
df_op = pd.read_parquet(Path(file_path + 'olist_order_payments_dataset.pq'))
df_or = pd.read_parquet(Path(file_path + 'olist_order_reviews_dataset.pq'))
df_p = pd.read_parquet(Path(file_path + 'olist_products_dataset.pq'))
df_s = pd.read_parquet(Path(file_path + 'olist_sellers_dataset.pq'))
df_c = pd.read_parquet(Path(file_path + 'olist_customers_dataset.pq'))
df_l = pd.read_parquet(Path(file_path + 'olist_geolocation_dataset.pq'))


df_oi, df_o = pp.merge_datasets(df_o = df_o, 
                  df_oi = df_oi,  
                   df_c = df_c,
                   df_or = df_or,
                   df_op = df_op,
                   df_geo_grouped = pp.preprocess_geo(df_l),
                   df_p = df_p,
                   df_s = df_s,
)

df_oi = eng.create_sellers_features(df_oi)
df_oi = eng.create_product_features(df_oi)
df_oi = eng.simple_fillna(df_oi, ['product_category_name', 'seller_state'])

df_o = eng.create_logistics_features(df_o = df_o)
df_o = eng.create_order_items_features(df_o = df_o, df_oi = df_oi)
df_o = eng.grouping_states_with_low_representativity(df_o, 1e3)
cols = ['payment_value', 'review_score', 'logistics_length', 'delay_length',  'product_volume', 'freight_value', 'product_photos_qty']

st.set_page_config(page_title="Training App",page_icon="🌍",layout="wide")
st.subheader("Example App")
st.markdown("##")

# fig, ax = plt.subplots(figsize = (12,10))
g = sns.clustermap(df_o[cols].dropna().corr(), center=0, cmap="vlag",
                   dendrogram_ratio=(.1, .2),
                   cbar_pos=(.02, .32, .03, .2),
                   linewidths=.75, figsize=(12, 13))
g.ax_row_dendrogram.remove()
st.pyplot(g)