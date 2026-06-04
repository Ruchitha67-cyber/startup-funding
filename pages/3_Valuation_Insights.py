import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.title("📈 Valuation Insights")

df = load_data()

fig = px.scatter(
    df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    size="Employees",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
