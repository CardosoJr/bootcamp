
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd

def clean_dataset(df, missing_limit):
    for c in df.columns:
        if df[c].isna().mean() > missing_limit:
            df.drop(columns = [c], inplace = True)
    return df.dropna()

def feature_engineering(df):
    df['Date'] = pd.to_datetime(df['Date'], format = "%d/%m/%Y")
    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    return df

def split_dataset(df, test_size, features, target):
    print(df.columns)
    print(features + [target])
    df = df[features + [target]]
    df_train, df_test = train_test_split(df, test_size = test_size)
    return df_train, df_test

def train_model(df_train, features, categorical_features, target):
    model_query = f"{target} ~ " + " + ".join([f"C({c})" for c in categorical_features]) + " + " + " + ".join([f for f in features if f not in categorical_features])
    model = smf.ols(model_query, df_train).fit()
    params = dict(model.params)
    return model, params

def predict_and_evaluate(model, df_test, target):
    y_hat = model.predict(df_test)
    metrics = { "MAE" : mean_absolute_error(y_hat, df_test[target])
               }
    
    return metrics
    

