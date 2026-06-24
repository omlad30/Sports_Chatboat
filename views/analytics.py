import streamlit as st
import pandas as pd
import sports_api
import numpy as np

st.title("📊 Team Analytics")
st.markdown("Deep dive visual analytics and performance tracking.")
st.divider()

teams = ["Arsenal", "Real Madrid", "Juventus", "Bayern Munich", "Chelsea", "Barcelona"]
selected_team = st.selectbox("Select a Team to Analyze", teams)

stats = sports_api.get_team_stats(selected_team)

st.subheader("Season Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Wins", stats['wins'])
col2.metric("Draws", stats['draws'])
col3.metric("Losses", stats['losses'])

st.divider()
st.subheader("Goals Breakdown")
chart_data = pd.DataFrame(
    [stats['goals_for'], stats['goals_against']],
    index=["Goals For", "Goals Against"],
    columns=["Count"]
)
st.bar_chart(chart_data, color="#38bdf8")

st.divider()
st.subheader("Recent Form (Expected vs Actual Goals)")
st.caption("Last 10 Games Analysis")
# Fake recent form data for visuals to show charting skills
form_data = pd.DataFrame(
    np.random.randn(10, 2) * 1.5 + 2,
    columns=["Expected Goals (xG)", "Actual Goals"]
)
st.line_chart(form_data, color=["#10b981", "#38bdf8"])
