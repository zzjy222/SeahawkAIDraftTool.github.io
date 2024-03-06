import streamlit as st
import time
import numpy as np

page_bg_img = """
<style>
[data-testid= "stAppViewContainer"] {
background-image: url("https://github.com/EloiseYiyunXu/AI-Chatbot.github.io/blob/main/static/bg.png?raw=true");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Upcoming Seahawks Events
upcoming_events = [
    {"date": "2024-04-25", "event": "NFL Draft Day", "location": "Las Vegas, NV","URL":"https://www.fordfield.com/events/detail/2024-nfl-draft#:~:text=The%202024%20NFL%20Draft%20presented,April%2025%E2%80%9327%2C%202024.&text=DETROIT%20%E2%80%93%20Visit%20Detroit%20announced%2C%20in,April%2025%2D27%2C%202024."},
    {"date": "2024-05-15", "event": "Seahawks Mini Camp", "location": "Virginia Mason Athletic Center", "URL":"https://www.seahawks.com/training-camp/attend/"},
    {"date": "2024-08-01", "event": "Preseason Game 1", "location": "Lumen Field", "URL":"https://www.seahawks.com/schedule/"},
    # Add more events as needed
]

st.header("Upcoming Seahawks Events")

for event in upcoming_events:
    st.subheader(f"{event['date']}: {event['event']}")
    st.write(f"Location: {event['location']}")
    st.write(f"URL: {event['URL']}")
    st.write("---")  # Add a separator line for readability
st.button("Re-run")