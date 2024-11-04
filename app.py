import streamlit as st
import streamlit.components.v1 as components

# Initialize session state for access control
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

# Access Code Entry for Hidden Page
access_code = "open-sesame"  # Replace with your secure passphrase

# Sidebar access code entry
with st.sidebar:
    if not st.session_state.access_granted:
        password = st.text_input("Enter Access Code:", type="password")
        if st.button("Submit"):
            if password == access_code:
                st.session_state.access_granted = True
                st.success("Access granted!")
            else:
                st.error("Incorrect access code.")

    # Display hidden page link if access is granted
    if st.session_state.access_granted:
        page_selection = st.radio("Navigate", ["Home", "Interventions"])
    else:
        page_selection = st.radio("Navigate", ["Home"])

# Display main or hidden page content based on selection
if page_selection == "Home":
    st.title("Survey")
    st.write("This survey will help us understand your background and current subjective mood. It should only take about 5 minutes to complete.")
    survey_url = "https://universityofalabama.az1.qualtrics.com/jfe/form/SV_6gnRQdY0zIUMtUO"
    iframe_code = f'<iframe src="{survey_url}" height="800px" width="600px"></iframe>'

    # Display the iframe in the Streamlit app
    components.html(iframe_code, height=800, width=600)
    
elif page_selection == "Interventions" and st.session_state.access_granted:
    st.title("Interventions")
    st.write("10-minute meditation from Calm")
    youtube_url = "https://www.youtube.com/watch?v=ZToicYcHIOU"
    st.video(youtube_url)
    st.write("Link in case of technical issues: https://www.youtube.com/watch?v=ZToicYcHIOU")
