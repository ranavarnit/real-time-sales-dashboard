# simple_sales_dashboard.py
# Simplified Streamlit Dashboard that actually works

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("📊 Real-Time Sales Analytics Dashboard")
st.markdown("---")

# Generate sample data
@st.cache_data
def generate_data():
    np.random.seed(42)
    n = 5000

    categories = ['Electronics', 'Fashion', 'Home', 'Books', 'Sports']
    regions = ['North', 'South', 'East', 'West', 'Central']
    channels = ['Online', 'Retail', 'Wholesale']

    data = {
        'timestamp': [datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23)) for _ in range(n)],
        'product_category': [random.choice(categories) for _ in range(n)],
        'region': [random.choice(regions) for _ in range(n)],
        'channel': [random.choice(channels) for _ in range(n)],
        'sales_amount': np.random.uniform(100, 50000, n),
        'quantity': np.random.randint(1, 10, n),
        'customer_id': [f"CUST_{random.randint(10000, 99999)}" for _ in range(n)]
    }

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    return df

# Load data
df = generate_data()

# Sidebar
st.sidebar.header("Controls")
date_range = st.sidebar.selectbox("Date Range", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])

days = {'Last 7 Days': 7, 'Last 30 Days': 30, 'Last 90 Days': 90}[date_range]
cutoff = datetime.now() - timedelta(days=days)

# Filter data
filtered_df = df[df['timestamp'] >= cutoff]

# KPIs
st.header("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Revenue", f"₹{filtered_df['sales_amount'].sum():,.0f}")
with col2:
    st.metric("Total Orders", f"{len(filtered_df):,}")
with col3:
    st.metric("Avg Order Value", f"₹{filtered_df['sales_amount'].mean():,.0f}")
with col4:
    st.metric("Unique Customers", f"{filtered_df['customer_id'].nunique():,}")

st.markdown("---")

# Charts
st.subheader("Sales by Category")
cat_sales = filtered_df.groupby('product_category')['sales_amount'].sum().reset_index()
fig1 = px.pie(cat_sales, values='sales_amount', names='product_category')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Sales Trend")
daily = filtered_df.groupby('date')['sales_amount'].sum().reset_index()
fig2 = px.line(daily, x='date', y='sales_amount')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Regional Performance")
regional = filtered_df.groupby('region')['sales_amount'].sum().reset_index()
fig3 = px.bar(regional, x='region', y='sales_amount', color='region')
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Sales by Channel")
channel_sales = filtered_df.groupby('channel')['sales_amount'].sum().reset_index()
fig4 = px.bar(channel_sales, x='channel', y='sales_amount', color='channel')
st.plotly_chart(fig4, use_container_width=True)
