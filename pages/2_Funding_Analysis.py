import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="Funding Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Funding Analysis Dashboard")
st.markdown("Analyze startup funding patterns and investment trends.")

# ---------------------------------------
# Load Data
# ---------------------------------------

df = load_data()

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------

st.sidebar.header("Filters")

industries = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

regions = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industries)) &
    (df["Region"].isin(regions))
]

# ---------------------------------------
# KPIs
# ---------------------------------------

total_funding = filtered_df[
    "Funding Amount (M USD)"
].sum()

avg_funding = filtered_df[
    "Funding Amount (M USD)"
].mean()

max_funding = filtered_df[
    "Funding Amount (M USD)"
].max()

avg_rounds = filtered_df[
    "Funding Rounds"
].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Funding",
    f"${total_funding:,.0f}M"
)

c2.metric(
    "Average Funding",
    f"${avg_funding:,.2f}M"
)

c3.metric(
    "Largest Funding",
    f"${max_funding:,.2f}M"
)

c4.metric(
    "Avg Funding Rounds",
    f"{avg_rounds:.1f}"
)

st.divider()

# ---------------------------------------
# Funding Distribution
# ---------------------------------------

st.subheader("Funding Distribution")

fig = px.histogram(
    filtered_df,
    x="Funding Amount (M USD)",
    nbins=30,
    color="Industry",
    title="Distribution of Funding Amounts"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------
# Industry Funding
# ---------------------------------------

col1, col2 = st.columns(2)

with col1:

    industry_funding = (
        filtered_df
        .groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry",
        text_auto=".2s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    region_funding = (
        filtered_df
        .groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_funding,
        names="Region",
        values="Funding Amount (M USD)",
        title="Regional Funding Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------
# Funding Rounds Analysis
# ---------------------------------------

st.subheader("Funding Rounds Analysis")

fig = px.box(
    filtered_df,
    x="Industry",
    y="Funding Rounds",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------
# Funding vs Valuation
# ---------------------------------------

st.subheader("Funding vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    size="Employees",
    color="Industry",
    hover_name="Startup Name",
    trendline="ols"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------
# Top Funded Startups
# ---------------------------------------

st.subheader("Top 10 Funded Startups")

top_funded = (
    filtered_df
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_funded[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Funding Amount (M USD)",
            "Valuation (M USD)"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------
# Funding Heatmap
# ---------------------------------------

st.subheader("Industry Funding Heatmap")

heatmap_data = (
    filtered_df
    .pivot_table(
        values="Funding Amount (M USD)",
        index="Industry",
        columns="Region",
        aggfunc="mean"
    )
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto",
    title="Average Funding by Industry and Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------
# Executive Insights
# ---------------------------------------

st.subheader("🧠 Funding Insights")

top_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

highest_startup = (
    filtered_df.loc[
        filtered_df[
            "Funding Amount (M USD)"
        ].idxmax(),
        "Startup Name"
    ]
)

st.success(
    f"🏆 Most funded industry: {top_industry}"
)

st.info(
    f"🌍 Highest investment region: {top_region}"
)

st.warning(
    f"🚀 Top funded startup: {highest_startup}"
)

# ---------------------------------------
# Download Data
# ---------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="funding_analysis.csv",
    mime="text/csv"
)
