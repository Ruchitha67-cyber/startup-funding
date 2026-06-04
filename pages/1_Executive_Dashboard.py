import streamlit as st

from utils.data_loader import load_data
from utils.metrics import calculate_metrics
from components.kpi_cards import display_kpis
from components.charts import funding_chart
from components.insights import generate_insights

st.title("📊 Executive Dashboard")

df = load_data()

metrics = calculate_metrics(df)

display_kpis(metrics)

st.divider()

funding_chart(df)

st.divider()

st.subheader("AI Insights")

for insight in generate_insights(df):
    st.success(insight)
