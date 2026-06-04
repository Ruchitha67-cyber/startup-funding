import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_data
from utils.metrics import get_metrics
from components.kpi_cards import display_kpis
from components.insights import generate_insights

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Filters")

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Region"].isin(region_filter))
]

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🚀 Executive Dashboard")
st.markdown(
    "Comprehensive overview of startup ecosystem performance."
)

st.divider()

# --------------------------------------------------
# KPI Section
# --------------------------------------------------

metrics = get_metrics(filtered_df)

display_kpis(metrics)

st.divider()

# --------------------------------------------------
# Row 1
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    funding_by_industry = (
        filtered_df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        funding_by_industry,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    valuation_by_region = (
        filtered_df.groupby("Region")
        ["Valuation (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        valuation_by_region,
        names="Region",
        values="Valuation (M USD)",
        title="Regional Valuation Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Revenue vs Valuation
# --------------------------------------------------

st.subheader("📈 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Market Share Analysis
# --------------------------------------------------

st.subheader("📊 Market Share Analysis")

fig = px.box(
    filtered_df,
    x="Industry",
    y="Market Share (%)",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Startup Age Analysis
# --------------------------------------------------

if "Year Founded" in filtered_df.columns:

    current_year = 2025

    filtered_df["Startup Age"] = (
        current_year -
        filtered_df["Year Founded"]
    )

    fig = px.histogram(
        filtered_df,
        x="Startup Age",
        nbins=20,
        title="Startup Age Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Executive Insights
# --------------------------------------------------

st.subheader("🧠 Executive Insights")

generate_insights(filtered_df)

# --------------------------------------------------
# Top Startups
# --------------------------------------------------

st.subheader("🏆 Top 10 Startups by Valuation")

top_startups = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_startups[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Revenue (M USD)",
            "Funding Amount (M USD)",
            "Valuation (M USD)"
        ]
    ],
    use_container_width=True
)

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------

with st.expander("📂 View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# --------------------------------------------------
# Download Data
# --------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv,
    file_name="startup_dashboard_data.csv",
    mime="text/csv"
)
