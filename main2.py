import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Load the data
data = pd.read_excel('tbl_yellow_boots.xlsx')
data['discount_rate'] = [max(1- i,0) for i in data['discount_rate']]
data['year_month'] = [str(i) for i in data['year_month'] ]

# Sidebar filters
st.sidebar.title("Filters")
selected_dealer_code = st.sidebar.multiselect("Select Dealer Code", data['dealer_code'].unique())
selected_article_description = st.sidebar.multiselect("Select Article Description", data['generic_article_description'].unique())
# Filter by year month

all_year_months = data['year_month'].unique().tolist()

# Add an option to select all year_month values
selected_year_months = st.sidebar.multiselect("Select Year-Month", all_year_months, default=all_year_months)

# Filter the data based on selected filters
filtered_data = data[(data['dealer_code'].isin(selected_dealer_code)) &
                     (data['generic_article_description'].isin(selected_article_description)) &
                     (data['year_month'].isin(selected_year_months))]

# Group the data by year_month and calculate the sum of selected columns
grouped_data = filtered_data.groupby('year_month')[['qty_sellin', 'sell_in_order_amt', 'sellout_amount', 'sellout_qty', 'discount_rate']].sum().reset_index()

# Create a Streamlit plot for the histogram
st.title("Histogram and Discount Rate")
y_axis = st.selectbox("Y-axis", ['qty_sellin', 'sell_in_order_amt', 'sellout_amount', 'sellout_qty'], index=0)

# Format x-axis labels to display as '202101' instead of '202.1k'
hist_fig = px.bar(grouped_data, x='year_month', y=y_axis, title=f'{y_axis} Over Time')
hist_fig.update_xaxes(type='category')
st.plotly_chart(hist_fig)

# Create a line plot for the discount rate
discount_fig = go.Figure()
discount_fig.add_trace(go.Scatter(x=grouped_data['year_month'], y=grouped_data['discount_rate'], mode='lines+markers', name='Discount Rate'))
discount_fig.update_xaxes(type='category', tickvals=grouped_data['year_month'], ticktext=grouped_data['year_month'])

discount_fig.update_layout(
    title='Discount Rate Over Time',
    xaxis_title='Year Month',
    yaxis_title='Discount Rate'
)
st.plotly_chart(discount_fig)