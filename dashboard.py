import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

sns.set(style='dark')

# Load Data
full_merged = pd.read_csv("full_merged.csv")
full_merged['order_purchase_timestamp'] = pd.to_datetime(full_merged['order_purchase_timestamp'])

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

st.title("🌐 E-commerce Data Analysis Dashboard")
st.sidebar.title("📊 Navigation")

# Sidebar Filters
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", full_merged['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", full_merged['order_purchase_timestamp'].max())

# Filter the dataset based on date range
filtered_data = full_merged[(full_merged['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                            (full_merged['order_purchase_timestamp'] <= pd.Timestamp(end_date))]

# Sidebar Navigation
page = st.sidebar.selectbox(
    "Choose a Page",
    ["Home", "Product Analysis", "Product Distribution", "Sales Trends", "Payment Insights"]
)

# Home Page
if page == "Home":
    st.header("📌 Project Overview")
    st.write("""
        Welcome to the **E-commerce Data Analysis Dashboard**.
        This interactive dashboard allows you to explore key metrics and trends in e-commerce, including:
        - Product performance
        - Sales trends
        - Payment insights
        - Distribution across regions
        Filter data using the options in the sidebar and navigate through different pages to dive deeper into the data.
    """)

    # Summary Statistics with Columns
    st.subheader("📊 Summary Statistics")
    col1, col2 = st.columns(2)

    total_transactions = len(filtered_data)
    avg_transaction_value = filtered_data['price'].mean()

    with col1:
        st.metric(label="Total Transactions", value=f"{total_transactions}")
    with col2:
        st.metric(label="Average Transaction Value (BRL)", value=f"{avg_transaction_value:.2f}")

    st.image("dashboard/ecommerce_banner.jpeg", use_container_width=True)

    st.header("✨ Highlights")

    # Richest Country by Total Revenue
    st.subheader("💰 Richest Country by Total Revenue")
    richest_country = filtered_data.groupby('customer_state')['price'].sum().idxmax()
    richest_country_revenue = filtered_data.groupby('customer_state')['price'].sum().max()
    st.write(f"**{richest_country}** is the richest country with a total revenue of **{richest_country_revenue:.2f} BRL**.")

    # Most Sold Product
    st.subheader("📦 Most Sold Product")
    most_sold_product = filtered_data.groupby('product_category_name_english')['order_id'].count().idxmax()
    most_sold_quantity = filtered_data.groupby('product_category_name_english')['order_id'].count().max()
    st.write(f"**{most_sold_product}** with **{most_sold_quantity}** units sold.")

    # Most Popular Payment Type
    st.subheader("💳 Most Popular Payment Type")
    most_popular_payment = filtered_data['payment_type'].mode()[0]
    st.write(f"The most popular payment method is **{most_popular_payment}**.")

# Product Analysis
elif page == "Product Analysis":
    st.header("Product Analysis")
    st.subheader("Top 10 Products by Total Revenue")
    top_products = filtered_data.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_products)

    st.subheader("Top 10 Products by Quantity Sold")
    top_products_quantity = filtered_data.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False).head(10)
    st.bar_chart(top_products_quantity)

# Product Distribution
elif page == "Product Distribution":
    st.subheader("Product Distribution by State")
    selected_state = st.selectbox("Select State", filtered_data['seller_state'].unique())
    state_data = filtered_data[filtered_data['seller_state'] == selected_state]
    category_total_value_by_state = state_data.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False)
    st.bar_chart(category_total_value_by_state)

# Sales Trends
elif page == "Sales Trends":
    st.header("Sales Trends")

    st.subheader("Monthly Sales Trends")
    filtered_data['order_month'] = filtered_data['order_purchase_timestamp'].dt.to_period('M')
    monthly_sales = filtered_data.groupby('order_month').size()
    st.line_chart(monthly_sales)

    st.subheader("Daily Sales Trends")
    daily_orders = filtered_data.groupby(filtered_data['order_purchase_timestamp'].dt.day_name())['order_id'].count().sort_values()
    st.line_chart(daily_orders)

    st.subheader("Distribution of Orders by Day of the Week")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#f0f0f0', '#e0e0e0', '#d0d0d0', '#c0c0c0', '#b0b0b0', '#a0a0a0', '#909090']
    ax.bar(daily_orders.index, daily_orders.values, color=colors, edgecolor='black')
    ax.set_title('Distribution of Orders by Day of the Week', fontsize=16)
    ax.set_xlabel('Day of the Week', fontsize=12)
    ax.set_ylabel('Number of Orders', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for i, v in enumerate(daily_orders.values):
        ax.text(i, v + 10, str(v), ha='center', color='black')
    plt.tight_layout()
    st.pyplot(fig)

# Payment Insights
elif page == "Payment Insights":
    st.header("Payment Insights")

    st.subheader("Average Payment Value by Payment Type")
    avg_payment_value_by_type = filtered_data.groupby('payment_type')['payment_value'].mean()
    st.bar_chart(avg_payment_value_by_type)

    st.subheader("Payment Type Distribution")
    payment_type_distribution = filtered_data['payment_type'].value_counts()
    st.bar_chart(payment_type_distribution)

st.write("Feel free to explore using the navigation menu on the left! 🚀")
