import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Load credentials 
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = st.secrets["gspread"]
creds_json = dict(st.secrets["gspread"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

client = gspread.authorize(creds)

# connect to google sheet
sheet = client.open("streamlit test").sheet1  # Replace with your Sheet name

# streamlit app
st.title("What's the Vibe?")

# dynamic list of emojiis
emojis = [":smile:", ":neutral_face:", ":confused:", ":pensive:", ":disappointed:", ":angry:", ":rage:"]

## form to log mood
st.subheader("Log a mood:")
with st.form("entry_form"):
    mood = st.radio(
        "What's the vibe?",
        options=emojis)
    # note option
    note = st.text_input("Optional note:", value="")
    # submission
    submitted = st.form_submit_button("Submit")
# add data to sheet
if submitted:
    timestamp = datetime.now().isoformat()
    sheet.append_row([timestamp, mood, note])
    st.success("Mood logged!")


## get data and plot
data = sheet.get_all_records()
df = pd.DataFrame(data)
# plot bar chart of moods for today
df["date"]=pd.to_datetime(df["timestamp"]).dt.date
today = pd.to_datetime("today").date()
print(df["date"])
print(today)
todaysmoods = df.loc[df["date"]==today, "mood"].value_counts()  # moods counts for today
fig, ax = plt.subplots()
ax.bar(todaysmoods.index, todaysmoods.values)
st.pyplot(fig)