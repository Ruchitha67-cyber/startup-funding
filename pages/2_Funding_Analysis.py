import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.title("💰 Funding Analysis")

df = load_data()

fig = px.histogram(
    df,
    x="Funding Amount (M USD)",
    color="Industry",
    nbins=40
)

st.plotly_chart(
    fig,
    use_container_width=True
)
