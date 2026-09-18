import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(
    page_title="Product Price Analyzer",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Product Price Analyzer")
st.write("Excel-Based Product Price Analysis Dashboard")

# Read Excel file
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXCEL_FILE = BASE_DIR / "products.xlsx"

df = pd.read_excel(EXCEL_FILE)

# Clean column names
df.columns = df.columns.str.strip()

# Convert Price and Rating to numbers
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Remove incomplete rows
df = df.dropna(subset=["Product", "Price", "Rating"])

# Sidebar
st.sidebar.header("🔍 Product Filter")

selected_products = st.sidebar.multiselect(
    "Select Products",
    df["Product"].tolist(),
    default=df["Product"].tolist()
)

# Filter data
filtered_df = df[df["Product"].isin(selected_products)]

# Check selection
if filtered_df.empty:
    st.warning("Please select at least one product.")
    st.stop()

# Dashboard metrics
st.subheader("📈 Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Products",
    len(filtered_df)
)

col2.metric(
    "Average Price",
    f"₹{filtered_df['Price'].mean():,.0f}"
)

col3.metric(
    "Lowest Price",
    f"₹{filtered_df['Price'].min():,.0f}"
)

col4.metric(
    "Highest Price",
    f"₹{filtered_df['Price'].max():,.0f}"
)

col5.metric(
    "Average Rating",
    f"{filtered_df['Rating'].mean():.2f} ⭐"
)

# Product data
st.subheader("📋 Product Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Charts
st.subheader("📊 Visual Analysis")

chart1, chart2 = st.columns(2)

# Bar Chart
with chart1:

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        filtered_df["Product"],
        filtered_df["Price"]
    )

    ax.set_xlabel("Product")
    ax.set_ylabel("Price (₹)")
    ax.set_title("Product Price Comparison")

    ax.tick_params(
        axis="x",
        rotation=45
    )

    fig.tight_layout()

    st.pyplot(fig)


# Scatter Plot
with chart2:

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(
        filtered_df["Price"],
        filtered_df["Rating"],
        s=100
    )

    ax.set_xlabel("Price (₹)")
    ax.set_ylabel("Rating")
    ax.set_title("Rating vs Price")

    ax.set_ylim(0, 5)

    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    st.pyplot(fig)


# Cheapest and expensive products
st.subheader("💡 Analysis")

cheapest = filtered_df.loc[
    filtered_df["Price"].idxmin()
]

expensive = filtered_df.loc[
    filtered_df["Price"].idxmax()
]

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"💰 Cheapest Product: **{cheapest['Product']}**\n\n"
        f"Price: ₹{cheapest['Price']:,.0f}"
    )

with col2:
    st.info(
        f"💎 Most Expensive Product: **{expensive['Product']}**\n\n"
        f"Price: ₹{expensive['Price']:,.0f}"
    )