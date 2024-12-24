import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')

# Load Data
full_merged = pd.read_csv("C:/Users/dgnat/OneDrive/Documents/VS Code/Dicoding/full_merged.csv")

st.title("E-commerce Data Analysis Dashboard")
st.sidebar.title("Navigation")

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Choose a Page",
    ["Home", "Product Analysis", "Sales Trends", "Payment Insights", "Advanced Visualizations"]
)

# Home Page
if page == "Home":
    st.header("Project Overview")
    st.write("""
        Welcome to the E-commerce Data Analysis Dashboard.
        This dashboard provides insights into product categories, sales trends, payment methods, and customer segmentation.
    """)
    # Summary Statistics
    total_transactions = len(full_merged)
    avg_transaction_value = full_merged['price'].mean()

    st.subheader("Summary Statistics")
    st.write(f"**Total Transactions:** {total_transactions}")
    st.write(f"**Average Transaction Value:** {avg_transaction_value:.2f} BRL")

# Product Analysis
elif page == "Product Analysis":
    st.header("Product Analysis")
    st.subheader("Top 10 Products by Revenue")
    top_products = full_merged.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_products)

    st.subheader("Top 10 Products by Quantity Sold")
    top_products_quantity = full_merged.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False).head(10)
    st.bar_chart(top_products_quantity)

    st.subheader("Top Product 10 Product Categories by State")
    selected_country = st.selectbox("Select Country", full_merged['seller_state'].unique()) 
    country_data = full_merged[full_merged['seller_state'] == selected_country]
    category_total_value_by_country = country_data.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False)
    st.bar_chart(category_total_value_by_country)

# Sales Trends
elif page == "Sales Trends":
    st.header("Sales Trends")
    st.subheader("Monthly Sales Trends")
    sales_trends = full_merged.groupby('order_month').size()
    st.line_chart(sales_trends)

    st.subheader("Weekly Sales Trends")
    full_merged['order_purchase_timestamp'] = pd.to_datetime(full_merged['order_purchase_timestamp'])
    full_merged['order_week'] = full_merged['order_purchase_timestamp'].dt.to_period('W')
    weekly_sales_trends = full_merged.groupby('order_week').size()
    st.bar_chart(weekly_sales_trends)

    st.subheader("Daily Sales Trends")
    daily_orders = full_merged.groupby.groupby(full_merged.groupby['order_purchase_timestamp'].dt.day_name()).size().sort_values()
    st.line_chart(daily_orders)

    st.subheader("Sales by Payment Type")
    sales_by_payment_type = full_merged.groupby('payment_type').size()
    st.bar_chart(sales_by_payment_type)

    st.subheader("Sales by Order Status")
    sales_by_order_status = full_merged.groupby('order_status').size()
    st.bar_chart(sales_by_order_status)

    st.subheader("Sales by Seller State and Order Status")
    sales_by_seller_state_and_order_status = full_merged.groupby(['seller_state', 'order_status']).size().unstack()
    st.bar_chart(sales_by_seller_state_and_order_status)

# Payment Insights
elif page == "Payment Insights":
    st.header("Payment Insights")
    st.subheader("Average Payment Value by Payment Type")
    avg_payment_value_by_type = full_merged.groupby('payment_type')['payment_value'].mean()
    st.bar_chart(avg_payment_value_by_type)

    st.subheader("Total Payment Value by Payment Type")
    total_payment_value_by_type = full_merged.groupby('payment_type')['payment_value'].sum()
    st.bar_chart(total_payment_value_by_type)

    st.subheader("Payment Type Distribution")
    payment_type_distribution = full_merged['payment_type'].value_counts()
    st.bar_chart(payment_type_distribution)

# Advanced Visualizations
elif page == "Advanced Visualizations":
    st.header("Advanced Visualizations")
    st.subheader("Heatmap: Payment Type by Order Status")
    heatmap_data = full_merged.pivot_table(
        index='payment_type', columns='order_status', values='payment_value', aggfunc='sum'
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Blues")
    plt.title("Payment Type by Order Status (Total Payment Value)")
    st.pyplot(plt)

st.write("Please, Feel Ease to Start Exploring by Click the Navigation Page On the Left ^_^")
st.write("Thank You for Exploring! 🚀")
st.image("https://drive.google.com/file/d/17cXSsPlpTKu_IsLIqZxo8GiJwmrkRMuC/view?usp=sharing", width=200) # Replace with your image path
