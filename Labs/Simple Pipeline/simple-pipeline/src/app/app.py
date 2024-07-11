import numpy as np
import pandas as pd
from plotly.offline import init_notebook_mode, iplot
import plotly.express as px
import plotly.figure_factory as FF
from plotly import tools
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import datetime
import streamlit as st

from pathlib import Path
import os
import sys

warnings.filterwarnings("ignore")

from src.simple_pipeline.pipelines.modeling.nodes import *

df = pd.read_parquet(Path("./data/02_intermediate/MELBOURNE_HOUSE_PRICES_LESS.pq"))
df = feature_engineering(df)


REGIONS = list(df['Regionname'].unique())
REGION_COLOR = dict(zip(REGIONS, ["#2E9AFE", "#FA5858", "#81F781", "#BE81F7", "#FE9A2E", "#04B4AE", "#088A08", "#8A0886"]))

def complementaryColor(my_hex):
    """Returns complementary RGB color

    Example:
    >>>complementaryColor('FFFFFF')
    '000000'
    """
    if my_hex[0] == '#':
        my_hex = my_hex[1:]
    rgb = (my_hex[0:2], my_hex[2:4], my_hex[4:6])
    comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
    return ''.join(comp)

def create_histogram_with_mean(data, name, marker_color):
  mean_price = np.mean(data)
  v, b = np.histogram(data, bins = 'auto')
  ylim = (np.max(v) / np.sum(v)) * 102
  xbins = go.XBins(start=b[0], end=b[-1], size=b[1] - b[0])  # Adjust as needed

  histogram_plot = go.Histogram(
      x=data,
      histnorm='percent',
      xbins = xbins,
      name=name,
      marker=dict(
          color=marker_color
      )
  )

  mean_line = go.Scatter(
      x=[mean_price, mean_price],
      y=[0, ylim],  # Set y-coordinates to span the entire histogram height
      mode='lines',
      name='Mean Price',
      line=dict(
          color= "#" + complementaryColor(marker_color),
          width=2,
          dash='dash'
      )
  )

  return [histogram_plot, mean_line]

overall_plots = create_histogram_with_mean(df['Price'].values, 'All Regions', '#6E6E6E')

region_plot = []
for region in REGIONS:
  region_plot.append(create_histogram_with_mean(df.query("Regionname == @region")['Price'].values, region, REGION_COLOR[region]))

gaussian_distribution_plot = create_histogram_with_mean(np.log(df['Price'].values), 'Log Price (All Regions)', '#800000')

suptitles = ['Overall Price Distribution'] + REGIONS + ['Distribution of Log Price']

fig = tools.make_subplots(rows=6, cols=2, print_grid=False, specs=[[{'colspan': 2}, None], [{}, {}], [{}, {}], [{}, {}], [{}, {}], [{'colspan': 2}, None]],
                         subplot_titles=suptitles)

fig.add_traces(overall_plots, 1, 1)

row_index = 2
col_index = 1
for p in region_plot:
  fig.add_traces(p, row_index, col_index)
  if col_index == 2:
    row_index += 1
    col_index = 0
  col_index += 1


fig.add_traces(gaussian_distribution_plot, 6, 1)

fig['layout'].update(showlegend=False, title="Price Distributions by Region",
                    height=1340, width=960)

st.plotly_chart(fig)
