import plotly.express as px
import streamlit as st

def funding_chart(df):

    funding = (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
