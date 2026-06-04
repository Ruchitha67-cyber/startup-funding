def get_metrics(df):

    return {
        "total_startups": len(df),
        "total_funding": df["Funding Amount (M USD)"].sum(),
        "avg_valuation": df["Valuation (M USD)"].mean(),
        "avg_revenue": df["Revenue (M USD)"].mean(),
        "profitable_pct": df["Profitable"].mean() * 100
    }
