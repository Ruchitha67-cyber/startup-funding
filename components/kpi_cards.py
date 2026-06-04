import streamlit as st

def display_kpis(metrics):

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric(
        "Startups",
        f"{metrics['total_startups']:,}"
    )

    c2.metric(
        "Funding",
        f"${metrics['total_funding']:,.0f}M"
    )

    c3.metric(
        "Valuation",
        f"${metrics['avg_valuation']:,.0f}M"
    )

    c4.metric(
        "Revenue",
        f"${metrics['avg_revenue']:,.0f}M"
    )

    c5.metric(
        "Profitable %",
        f"{metrics['profitable_pct']:.1f}%"
    )
