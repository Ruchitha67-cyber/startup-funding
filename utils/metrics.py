def get_metrics(df):

    return {
        "total_startups": len(df),
        "total_funding": df["Funding Amount (M USD)"].sum(),
        "avg_valuation": df["Valuation (M USD)"].mean()
    }
