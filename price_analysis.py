import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="Product Price Comparison",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 Web Scraping & Product Price Comparison System")

st.write(
    "Compare product prices and ratings across "
    "Amazon, Flipkart, Meesho and Myntra."
)

# Excel file location
BASE_DIR = Path(__file__).resolve().parent
EXCEL_FILE = BASE_DIR / "products.xlsx"

# Read Excel
df = pd.read_excel(EXCEL_FILE)

# Clean column names
# Clean column names
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace("\n", " ", regex=False)
)

# Show detected columns

# Check required columns
required_columns = ["Platform", "Product", "Price", "Rating"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing columns in products.xlsx: {missing_columns}"
    )
    st.info(
        "Your Excel file must contain exactly these columns: "
        "Platform, Product, Price, Rating"
    )
    st.stop()

# Convert Price and Rating
df["Price"] = pd.to_numeric(
    df["Price"], errors="coerce"
)

df["Rating"] = pd.to_numeric(
    df["Rating"], errors="coerce"
)

# Remove invalid rows
df = df.dropna(
    subset=["Platform", "Product", "Price", "Rating"]
)
# Sidebar filters
st.sidebar.header("🔍 Filters")

platforms = st.sidebar.multiselect(
    "Select Websites",
    sorted(df["Platform"].unique()),
    default=sorted(df["Platform"].unique())
)

products = st.sidebar.multiselect(
    "Select Products",
    sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

# Filter data
filtered_df = df[
    (df["Platform"].isin(platforms)) &
    (df["Product"].isin(products))
]

if filtered_df.empty:
    st.warning("Please select at least one website and one product.")
    st.stop()

# Summary
st.subheader("📊 Overall Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Records",
    len(filtered_df)
)

col2.metric(
    "Products",
    filtered_df["Product"].nunique()
)

col3.metric(
    "Websites",
    filtered_df["Platform"].nunique()
)

col4.metric(
    "Average Price",
    f"₹{filtered_df['Price'].mean():,.0f}"
)

col5.metric(
    "Average Rating",
    f"{filtered_df['Rating'].mean():.2f} ⭐"
)

# Data table
st.subheader("📋 Product Data")

display_df = filtered_df.copy()

display_df["Price"] = display_df["Price"].apply(
    lambda x: f"₹{x:,.0f}"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Price comparison
st.subheader("💰 Price Comparison")

price_table = filtered_df.pivot_table(
    index="Product",
    columns="Platform",
    values="Price",
    aggfunc="min"
)

fig, ax = plt.subplots(figsize=(12, 6))

price_table.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Product Price Comparison Across Websites"
)

ax.set_xlabel("Product")
ax.set_ylabel("Price (₹)")

ax.tick_params(
    axis="x",
    rotation=45
)

ax.legend(title="Website")

fig.tight_layout()

st.pyplot(fig)

# Rating comparison
st.subheader("⭐ Rating Comparison")

rating_table = filtered_df.pivot_table(
    index="Product",
    columns="Platform",
    values="Rating",
    aggfunc="mean"
)

fig, ax = plt.subplots(figsize=(12, 6))

rating_table.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Product Rating Comparison Across Websites"
)

ax.set_xlabel("Product")
ax.set_ylabel("Rating")

ax.set_ylim(0, 5)

ax.tick_params(
    axis="x",
    rotation=45
)

ax.legend(title="Website")

fig.tight_layout()

st.pyplot(fig)

# Price vs Rating
st.subheader("📈 Price vs Rating")

fig, ax = plt.subplots(figsize=(10, 6))

for platform in filtered_df["Platform"].unique():

    platform_data = filtered_df[
        filtered_df["Platform"] == platform
    ]

    ax.scatter(
        platform_data["Price"],
        platform_data["Rating"],
        s=100,
        label=platform
    )

ax.set_title("Price vs Rating")

ax.set_xlabel("Price (₹)")
ax.set_ylabel("Rating")

ax.set_ylim(0, 5)

ax.grid(True, alpha=0.3)

ax.legend()

fig.tight_layout()

st.pyplot(fig)

# Cheapest website
st.subheader("🏆 Cheapest Website for Each Product")

cheapest_rows = filtered_df.loc[
    filtered_df.groupby("Product")["Price"].idxmin()
]

cheapest_display = cheapest_rows[
    ["Product", "Platform", "Price", "Rating"]
].copy()

cheapest_display["Price"] = cheapest_display["Price"].apply(
    lambda x: f"₹{x:,.0f}"
)

st.dataframe(
    cheapest_display,
    use_container_width=True,
    hide_index=True
)

# Highest price
st.subheader("💎 Highest Price for Each Product")

expensive_rows = filtered_df.loc[
    filtered_df.groupby("Product")["Price"].idxmax()
]

expensive_display = expensive_rows[
    ["Product", "Platform", "Price", "Rating"]
].copy()

expensive_display["Price"] = expensive_display["Price"].apply(
    lambda x: f"₹{x:,.0f}"
)

st.dataframe(
    expensive_display,
    use_container_width=True,
    hide_index=True
)

# Price difference
st.subheader("💸 Price Difference")

price_difference = (
    filtered_df
    .groupby("Product")["Price"]
    .agg(["min", "max"])
)

price_difference["Difference"] = (
    price_difference["max"]
    - price_difference["min"]
)

price_difference = price_difference.reset_index()

price_difference = price_difference.rename(
    columns={
        "min": "Lowest Price",
        "max": "Highest Price"
    }
)

price_difference["Lowest Price"] = price_difference[
    "Lowest Price"
].apply(lambda x: f"₹{x:,.0f}")

price_difference["Highest Price"] = price_difference[
    "Highest Price"
].apply(lambda x: f"₹{x:,.0f}")

price_difference["Difference"] = price_difference[
    "Difference"
].apply(lambda x: f"₹{x:,.0f}")

st.dataframe(
    price_difference,
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("---")

st.write(
    "📌 Data Source: Web-scraped product information stored in Excel."
)

st.write(
    "🛒 Platforms: Amazon | Flipkart | Meesho | Myntra"
)
