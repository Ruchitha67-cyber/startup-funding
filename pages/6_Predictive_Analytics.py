import streamlit as st

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from utils.data_loader import load_data

st.title("🤖 Predictive Analytics")

df = load_data()

features = [
    "Funding Rounds",
    "Funding Amount (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)"
]

X = df[features]
y = df["Valuation (M USD)"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor()

model.fit(X_train, y_train)

score = model.score(X_test, y_test)

st.metric(
    "Prediction Accuracy",
    f"{score:.2%}"
)
