import pandas as pd 
import numpy as np

def preprocess_geo(df_geo: pd.DataFrame) -> pd.DataFrame:
    return df_geo.groupby('geolocation_zip_code_prefix')[['geolocation_lat', 'geolocation_lng']].mean().reset_index()

def merge_datasets(df_o: pd.DataFrame, 
                   df_oi: pd.DataFrame,
                   df_c: pd.DataFrame,
                   df_or: pd.DataFrame,
                   df_op: pd.DataFrame,
                   df_geo_grouped: pd.DataFrame,
                   df_p: pd.DataFrame,
                   df_s: pd.DataFrame,
                   ) -> pd.DataFrame:
    df_o = pd.merge(left = df_o, right = df_c, on = ['customer_id'], how = 'left')
    df_o = pd.merge(left = df_o, right = df_op.groupby('order_id')['payment_value'].sum(), on = ['order_id'], how = 'left')
    df_o = pd.merge(left = df_o, right = df_or.groupby('order_id')['review_score'].mean().reset_index(), 
                    on = ['order_id'], 
                    how = 'left')
    df_o = pd.merge(left = df_o, 
                    right = df_geo_grouped.rename(columns = {'geolocation_lat' : 'c_lat',	'geolocation_lng' : 'c_lng'}), 
                    left_on = 'customer_zip_code_prefix',
                    right_on = 'geolocation_zip_code_prefix',
                    how = 'left')

    df_oi = pd.merge(left = df_oi, right = df_p, on = ['product_id'], how = 'left')
    df_oi = pd.merge(left = df_oi, right = df_s, on = ['seller_id'], how = 'left')
    df_oi = pd.merge(left = df_oi, 
                    right = df_geo_grouped.rename(columns = {'geolocation_lat' : 's_lat',	'geolocation_lng' : 's_lng'}),
                    left_on = 'seller_zip_code_prefix',
                    right_on = 'geolocation_zip_code_prefix', 
                    how = 'left')
    
    return pd.merge(left = df_oi, right = df_o, on = ['order_id'], how = 'left'), df_o
