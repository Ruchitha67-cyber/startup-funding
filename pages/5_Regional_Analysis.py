import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.title("🌍 Regional Analysis")

df = load_data()

region = (
    df.groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region,
    names="Region",
    values="Valuation (M USD)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
