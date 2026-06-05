import streamlit as st
import json
import os

FILE_NAME = "study_history.json"


def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []


st.title("📊 Jarvis Study Dashboard")

data = load_data()

if not data:
    st.warning("No study data yet.")
    st.stop()

totals = {}

for s in data:
    subject = s["subject"]
    duration = s["duration_minutes"]
    totals[subject] = totals.get(subject, 0) + duration


st.subheader("Study Table")

st.table([
    {"Subject": k, "Minutes": round(v, 2)}
    for k, v in totals.items()
])


st.subheader("📈 Chart")

st.bar_chart(totals)


st.subheader("🧠 Insights")

weak = min(totals, key=totals.get)
strong = max(totals, key=totals.get)

st.info(f"Weak Subject: {weak}")
st.success(f"Strong Subject: {strong}")