import streamlit as st
from twilio.rest import Client


# Access Twilio credentials from Streamlit secrets
account_sid = st.secrets["twilio"]["account_sid"]
auth_token = st.secrets["twilio"]["auth_token"]

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Send SMS (note: Will want to replace the survey link with the streamlit website link once the website is published)
message = client.messages.create(
    body="Link to my research survey: https://universityofalabama.az1.qualtrics.com/jfe/form/SV_6gnRQdY0zIUMtUO",
    from_='+18666433631',  # Twilio phone number
    to='+18777804236'      # Recipient's phone number
)

# Print message SID to confirm it was sent
st.write(f"Message sent with SID: {message.sid}")
