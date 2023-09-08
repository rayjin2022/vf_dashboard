import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
data = pd.read_excel('tbl_yellow_boots.xlsx')
data['discount_rate'] = [max(1 - i, 0) for i in data['discount_rate']]
data['year_month'] = [str(i) for i in data['year_month']]

# Sidebar filters
st.sidebar.title("Filters")
selected_dealer_code = st.sidebar.multiselect("Select Dealer Code", data['dealer_code'].unique())
selected_article_description = st.sidebar.multiselect("Select Article Description", data['generic_article_description'].unique())

# Filter by year month
all_year_months = data['year_month'].unique().tolist()

# Default selection for year_month
default_year_months = ['202103', '202104', '202105', '202106', '202107', '202108', '202109',
                       '202110', '202111', '202112', '202201', '202202', '202203', '202204',
                       '202205', '202206', '202207', '202208', '202209', '202210', '202211',
                       '202212', '202301']

# Ensure that all default values exist in all_year_months
default_year_months = [month for month in default_year_months if month in all_year_months]

# Add an option to select year_month values
selected_year_months = st.sidebar.multiselect("Select Year-Month", all_year_months, default=default_year_months)

# Filter the data based on selected filters
filtered_data = data[(data['dealer_code'].isin(selected_dealer_code)) &
                     (data['generic_article_description'].isin(selected_article_description)) &
                     (data['year_month'].isin(selected_year_months))]

# Group the data by year_month and calculate the sum of selected columns
grouped_data = filtered_data.groupby('year_month')[['sellout_amount', 'discount_rate']].sum().reset_index()

# Create a Streamlit plot for the histogram and line chart
st.title("Double Axis Plot: Sell Amount and Discount Rate Over Time")
fig = go.Figure()

# Add the histogram (sell amount)
fig.add_trace(go.Bar(x=grouped_data['year_month'], y=grouped_data['sellout_amount'], name='Sell Amount', yaxis='y'))

# Add the line plot (discount rate)
fig.add_trace(go.Scatter(x=grouped_data['year_month'], y=grouped_data['discount_rate'], mode='lines+markers', name='Discount Rate', yaxis='y2'))

# Update the layout for dual y-axes
fig.update_layout(
    xaxis=dict(type='category', tickvals=grouped_data['year_month'], ticktext=grouped_data['year_month'], title='Year Month'),
    yaxis=dict(title='Sell Amount', rangemode='tozero'),
    yaxis2=dict(title='Discount Rate', overlaying='y', side='right', rangemode='tozero'),
    title_text="Sell Amount and Discount Rate Over Time",
)

# Display the plot
st.plotly_chart(fig)
