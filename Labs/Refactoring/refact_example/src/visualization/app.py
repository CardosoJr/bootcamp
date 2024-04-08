import streamlit as st
import pandas as pd
import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))
print(sys.path)

import src.visualization.visualize as viz
import src.models.train as train

df = pd.read_parquet("https://raw.githubusercontent.com/CardosoJr/bootcamp/main/Datasets/Melbourne/MELBOURNE_HOUSE_PRICES_LESS.pq")
df = df.dropna()

model = train.train_lin_reg(df)

st.header('Dashboard para previsão de preços de imóveis')
st.plotly_chart(viz.visualize_prices(df), use_container_width=True)

rooms = st.number_input("Number of Rooms:", min_value=1, max_value=20, value=3)
distance = st.number_input("Distance from City Center (km):", min_value=0.0, max_value=100.0, value=5.0)
propertycount = st.number_input("Property Count in the Area:", min_value=1, value=1000)


if st.button("Calculate Price"):
    input_data = pd.DataFrame({'Rooms': [rooms], 'Distance': [distance], 'Propertycount': [propertycount]})
    predicted_price = model.predict(input_data)[0]
    st.write(f"Predicted Price: ${predicted_price:,.2f}")