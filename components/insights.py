def generate_insights(df):

    insights = []

    top_industry = (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .idxmax()
    )

    insights.append(
        f"🏆 Highest valuation industry: {top_industry}"
    )

    return insights
