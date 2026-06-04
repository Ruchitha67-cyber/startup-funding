def preprocess_data(df):

    df = df.drop_duplicates()
    df = df.dropna()

    if "Year Founded" in df.columns:
        df["Startup Age"] = 2025 - df["Year Founded"]

    return df
