# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Financial Performance Dashboard",
    page_icon="💹",
    layout="wide",
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/financial_data.csv")
    df["Month"] = pd.Categorical(df["Month"], categories=[
        "Jan-2024", "Feb-2024", "Mar-2024", "Apr-2024", "May-2024", "Jun-2024",
        "Jul-2024", "Aug-2024", "Sep-2024", "Oct-2024", "Nov-2024", "Dec-2024"
    ], ordered=True)
    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filter Data")

regions = st.sidebar.multiselect(
    "Select Region(s):",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Filter data
filtered_df = df[df["Region"].isin(regions)]

# -------------------------------
# KPI Metrics
# -------------------------------
st.title("📊 Financial Performance Dashboard")

total_revenue = filtered_df["Revenue"].sum()
total_expenses = filtered_df["Expenses"].sum()
total_profit = filtered_df["Profit"].sum()
avg_margin = filtered_df["Net_Profit_Margin"].mean() * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("💸 Total Expenses", f"${total_expenses:,.0f}")
col3.metric("📈 Total Profit", f"${total_profit:,.0f}")
col4.metric("📊 Avg. Profit Margin", f"{avg_margin:.2f}%")

st.markdown("---")

# -------------------------------
# Visualizations
# -------------------------------

# 1️⃣ Monthly Trend of Revenue, Expenses, and Profit
st.subheader("📆 Monthly Financial Trends")
trend_df = filtered_df.groupby("Month")[["Revenue", "Expenses", "Profit"]].sum().reset_index()
fig_trend = px.line(trend_df, x="Month", y=["Revenue", "Expenses", "Profit"],
                    markers=True, title="Revenue vs Expenses vs Profit (Monthly)")
st.plotly_chart(fig_trend, use_container_width=True)

# 2️⃣ Regional Performance
st.subheader("🌎 Regional Performance Overview")
region_df = filtered_df.groupby("Region")[["Revenue", "Expenses", "Profit"]].sum().reset_index()
fig_region = px.bar(region_df, x="Region", y=["Revenue", "Expenses", "Profit"],
                    barmode="group", title="Regional Financial Summary")
st.plotly_chart(fig_region, use_container_width=True)

# 3️⃣ Profit Margin by Region
st.subheader("💹 Average Profit Margin by Region")
margin_df = filtered_df.groupby("Region")["Net_Profit_Margin"].mean().reset_index()
margin_df["Net_Profit_Margin"] = margin_df["Net_Profit_Margin"] * 100
fig_margin = px.bar(margin_df, x="Region", y="Net_Profit_Margin",
                    text_auto=".2f", title="Profit Margin (%) by Region", color="Region")
st.plotly_chart(fig_margin, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Created by [Your Name] | Sample Financial Dashboard for Business Analyst Portfolio")
