import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------

st.title("🚀 Startup Executive Dashboard")
st.markdown("High-Level Business Intelligence & Performance Analytics")

st.divider()

# --------------------------------------------------
# KPI Section
# --------------------------------------------------

total_startups = len(df)

total_funding = df["Funding Amount (M USD)"].sum()

avg_valuation = df["Valuation (M USD)"].mean()

avg_revenue = df["Revenue (M USD)"].mean()

profitable_pct = (
    df["Profitable"].mean() * 100
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Startups",
    f"{total_startups:,}"
)

c2.metric(
    "Total Funding",
    f"${total_funding:,.0f}M"
)

c3.metric(
    "Avg Valuation",
    f"${avg_valuation:,.0f}M"
)

c4.metric(
    "Avg Revenue",
    f"${avg_revenue:,.0f}M"
)

c5.metric(
    "Profitable %",
    f"{profitable_pct:.1f}%"
)

st.divider()

# --------------------------------------------------
# Row 1
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    funding_industry = (
        df.groupby("Industry")["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        funding_industry,
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

    valuation_industry = (
        df.groupby("Industry")["Valuation (M USD)"]
        .mean()
        .reset_index()
        .sort_values(
            "Valuation (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        valuation_industry,
        x="Industry",
        y="Valuation (M USD)",
        title="Average Valuation by Industry",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Row 2
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        size="Employees",
        color="Industry",
        hover_name="Startup Name",
        title="Revenue vs Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    region_data = (
        df.groupby("Region")
        ["Valuation (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_data,
        names="Region",
        values="Valuation (M USD)",
        title="Regional Valuation Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Market Share Analysis
# --------------------------------------------------

st.subheader("📈 Market Share Distribution")

fig = px.box(
    df,
    x="Industry",
    y="Market Share (%)",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Startup Lifecycle Analysis
# --------------------------------------------------

if "Year Founded" in df.columns:

    current_year = 2025

    df["Startup Age"] = (
        current_year -
        df["Year Founded"]
    )

    fig = px.scatter(
        df,
        x="Startup Age",
        y="Valuation (M USD)",
        color="Industry",
        size="Funding Amount (M USD)",
        title="Startup Age vs Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# AI Insights Section
# --------------------------------------------------

st.subheader("🧠 Executive Insights")

top_industry = (
    df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

highest_funding = (
    df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    df.groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

st.success(
    f"🏆 Highest Valuation Industry: {top_industry}"
)

st.info(
    f"💰 Most Funded Industry: {highest_funding}"
)

st.warning(
    f"🌍 Top Performing Region: {top_region}"
)

# --------------------------------------------------
# Raw Dataset
# --------------------------------------------------

with st.expander("View Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
