import streamlit as st
import sports_api

st.title("🔴 Live Match Scores")
st.markdown("Real-time match data integration. (Data fetched via external API)")
st.divider()

with st.spinner("Fetching live scores..."):
    scores = sports_api.get_live_scores()

for match in scores:
    # Use a custom container that inherits some of our CSS
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{match['home']}** vs **{match['away']}**")
            st.caption(match['league'])
        with col2:
            st.subheader(match['score'])
        with col3:
            if "Finished" in match['status']:
                st.markdown(f"*{match['status']}*")
            else:
                st.markdown(f"**🔴 {match['status']}**")
    st.markdown("---")
