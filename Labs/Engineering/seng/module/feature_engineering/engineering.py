import pandas as pd 
import numpy as np
import geopy.distance
import category_encoders as ce

state_region_map = {
    'AC': 'N', 'AP': 'N', 'AM': 'N', 'PA': 'N', 'RO': 'N', 'RR': 'N', 'TO': 'N',
    'AL': 'NE', 'BA': 'NE', 'CE': 'NE', 'MA': 'NE', 'PB': 'NE', 'PE': 'NE', 'PI': 'NE', 'RN': 'NE', 'SE': 'NE',
    'ES': 'SE', 'MG': 'SE', 'RJ': 'SE', 'SP': 'SE',
    'PR': 'S', 'RS': 'S', 'SC': 'S',
    'GO': 'CO', 'MT': 'CO', 'MS': 'CO', 'DF': 'CO'
}

def calculate_distance(data: list):
    try:
        return geopy.distance.geodesic((data['c_lat'], data['c_lng']), (data['s_lat'], data['s_lng'])).km
    except:
        return 0
    
def create_sellers_features(df_oi: pd.DataFrame) -> pd.DataFrame:
    # df_oi['customer_seller_distance'] = df_oi.apply(calculate_distance, axis = 1)
    df_oi['customer_seller_distance']  = [0] * len(df_oi)
    df_s = df_oi.groupby('seller_id').agg({'price' : 'sum', 'order_item_id' : 'count'}).reset_index().rename(columns = {'price' : 's_total_volume', 'order_item_id' : 's_total_items'})
    df_oi = pd.merge(left = df_oi, right = df_s, on = 'seller_id', how = 'left')
    return df_oi

def create_product_features(df_oi: pd.DataFrame) -> pd.DataFrame:
    df_oi['product_volume'] = df_oi[['product_length_cm','product_height_cm','product_width_cm']].prod(axis =1)
    return df_oi

def create_logistics_features(df_o: pd.DataFrame) -> pd.DataFrame:
    df_o['logistics_length'] = (df_o['order_delivered_customer_date'] - df_o['order_approved_at']).dt.days
    df_o['delay_length'] = (df_o['order_delivered_customer_date'] - df_o['order_estimated_delivery_date']).dt.days
    df_o['is_delayed'] = (df_o['delay_length'] > 0) * 1
    return df_o

def create_order_items_features(df_oi: pd.DataFrame,
                                df_o: pd.DataFrame) -> pd.DataFrame:
    
    df_oi_g = df_oi.groupby('order_id').agg({'customer_seller_distance' : 'max',
                               'product_volume' : 'sum',
                               'product_weight_g' : 'sum',
                               'product_photos_qty' : 'sum',
                               'freight_value' : 'sum',
                               'order_item_id' : 'count',
                               'shipping_limit_date' : 'min',
                               'product_category_name' : lambda x: x.mode()[0],
                               'seller_state' : lambda x: x.mode()[0],
                               's_total_volume' : 'mean',
                               's_total_items' : 'mean',
                              }).reset_index()
    
    df_o = pd.merge(left = df_o, right = df_oi_g, on = ['order_id'], how = 'left')
    df_o['freight_ratio'] = df_o['freight_value'] / df_o['payment_value']

    return df_o

def simple_fillna(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for c in columns:
        df[c].fillna("unknown", inplace = True)
    return df

def grouping_states_with_low_representativity(df_o: pd.DataFrame, threshold: float) -> pd.DataFrame:
    vc = df_o['customer_state'].value_counts()
    mapping = {x[0]:x[0] if x[1] > threshold else state_region_map[x[0]] for x in vc.items()}
    df_o['customer_state'] = df_o['customer_state'].map(mapping)
    df_o['seller_state'] = df_o['seller_state'].map(mapping)

    return df_o