import streamlit as st
import pandas as pd
import plotly.express as px
# Load the data
data = pd.read_csv('tbl_yellow_boots.csv')

# Sidebar filters
st.sidebar.title("Filters")
selected_dealer_code = st.sidebar.multiselect("Select Dealer Code", data['dealer_code'].unique())
selected_article_description = st.sidebar.multiselect("Select Article Description", data['generic_article_description'].unique())

# Filter the data based on selected filters
filtered_data = data[(data['dealer_code'].isin(selected_dealer_code)) & (data['generic_article_description'].isin(selected_article_description))]

# Group the data by year_month and calculate the sum of selected columns
grouped_data = filtered_data.groupby('year_month')[['qty_sellin', 'sell_in_order_amt', 'sellout_amount', 'sellout_qty']].sum().reset_index()

# Line plot using Plotly
st.title("Line Plot")
y_axis = st.selectbox("Y-axis", ['qty_sellin', 'sell_in_order_amt', 'sellout_amount', 'sellout_qty'], index=0)

fig = px.line(grouped_data, x='year_month', y=y_axis, title=f'{y_axis} Over Time')
st.plotly_chart(fig)
