import pandas as pd
import numpy as np 

import module.data.preprocessing as pp
import module.data.problem_definition as problem
import module.data.split as split
import module.feature_engineering.engineering as eng
import module.feature_engineering.encoding as enc
import hashlib

def get_raw_hash(df_o: pd.DataFrame, 
                   df_oi: pd.DataFrame,
                   df_c: pd.DataFrame,
                   df_or: pd.DataFrame,
                   df_op: pd.DataFrame,
                   df_l: pd.DataFrame,
                   df_p: pd.DataFrame,
                   df_s: pd.DataFrame,
                   ) -> dict:
    
    hash = { "order" : hashlib.sha256(df_o.sort_index(axis=1).to_string().encode()).hexdigest(),
             "order_items" : hashlib.sha256(df_oi.sort_index(axis=1).to_string().encode()).hexdigest(), 
             "customers" : hashlib.sha256(df_c.sort_index(axis=1).to_string().encode()).hexdigest(), 
             "order_reviews" : hashlib.sha256(df_or.sort_index(axis=1).to_string().encode()).hexdigest(), 
             "order_payments" : hashlib.sha256(df_op.sort_index(axis=1).to_string().encode()).hexdigest(), 
             "geolocalization" : hashlib.sha256(df_l.sort_index(axis=1).to_string().encode()).hexdigest(), 
             "products" : hashlib.sha256(df_p.sort_index(axis=1).to_string().encode()).hexdigest(), 
             "sellers" : hashlib.sha256(df_s.sort_index(axis=1).to_string().encode()).hexdigest(), 
    }

    return hash, hash

def prepare_and_merge(df_o: pd.DataFrame, 
                   df_oi: pd.DataFrame,
                   df_c: pd.DataFrame,
                   df_or: pd.DataFrame,
                   df_op: pd.DataFrame,
                   df_l: pd.DataFrame,
                   df_p: pd.DataFrame,
                   df_s: pd.DataFrame,
                   ) -> pd.DataFrame:
            
    for c in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',	'order_delivered_customer_date', 'order_estimated_delivery_date']:
        df_o[c] = pd.to_datetime(df_o[c])

    for c in ['shipping_limit_date']:
        df_oi[c] = pd.to_datetime(df_oi[c])

    df_oi, df_o = pp.merge_datasets(df_o = df_o, 
                  df_oi = df_oi,  
                   df_c = df_c,
                   df_or = df_or,
                   df_op = df_op,
                   df_geo_grouped = pp.preprocess_geo(df_l),
                   df_p = df_p,
                   df_s = df_s,
                )
    
    return df_oi, df_o

def order_items_engineering(df_oi: pd.DataFrame) -> pd.DataFrame:
    df_oi = eng.create_sellers_features(df_oi)
    df_oi = eng.create_product_features(df_oi)
    df_oi = eng.simple_fillna(df_oi, ['product_category_name', 'seller_state'])
    return df_oi

def orders_engineering(df_o: pd.DataFrame) -> pd.DataFrame:
    df_o = eng.create_logistics_features(df_o = df_o)
    return df_o

def create_finaldataset(df_o: pd.DataFrame, df_oi: pd.DataFrame, params) -> pd.DataFrame:
    df_o = eng.create_order_items_features(df_o = df_o, df_oi = df_oi)
    df_o = eng.grouping_states_with_low_representativity(df_o, 1e3)

    drop_cols = [x for x in df_o.columns if x not in params['numerical'] + params['categorical']]
    df_o.drop(columns = drop_cols, inplace = True)

    p = problem.BinaryClassProblem(target = params['initial_target'], data = df_o)
    if params['problem'] != "binary":
        p = problem.MultClassProblem(target = params['initial_target'], data = df_o) 
    
    return p.get_data()

def split_dataset(df_o: pd.DataFrame, params):
    train_data = []
    val_data = []
    if params['method'] == 'kfold':
        splitter = split.KFoldSplit(seed = 42, num_folds = params['params']['num_split'])
        idx = splitter.fit_transform(df_o)

        for idx_train, idx_test in idx:
            train_data.append(df_o.loc[idx_train])
            val_data.append(df_o.loc[idx_test])
    else:
        splitter = split.Split(seed = 42, validation_size = None, test_size = params['params']['test_size'])
        idx_train, idx_validation, idx_test = splitter.fit_transform(df_o)
        train_data.append(df_o.loc[idx_train])
        val_data.append(df_o.loc[idx_test])

    return tuple(train_data + val_data)

def encode(df_train: pd.DataFrame, df_val: pd.DataFrame, params):
    convert_structure = {}
    for method, cols in params['pre_processing'].items():
        convert_structure[method] = {'cols' : cols, 'target' : 'target'}
    encoder = enc.Encoding(convert_structure = convert_structure)

    encoder.fit(df_train)
    df_train = encoder.transform(df_train)
    df_val = encoder.transform(df_val)

    return df_train, df_val