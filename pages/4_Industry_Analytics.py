import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.title("🏭 Industry Analytics")

df = load_data()

industry = (
    df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    industry,
    x="Industry",
    y="Valuation (M USD)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
