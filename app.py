import streamlit as st
import streamlit.components.v1 as components
import boto3

def get_access_code():
    # Load AWS credentials
    aws_access_key = st.secrets["ACCESS_KEY"]
    aws_secret_key = st.secrets["SECRET_KEY"]
    aws_region = "us-east-2"

    # Load SSM
    ssm = boto3.client(
    "ssm",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
    )

    # Fetch daily access code
    try:
        response = ssm.get_parameter(Name="/streamlit/access_code", WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as e:
        st.error("Failed to retrieve access code.")
        return None
    

# Initialize session state for access control
if "access_intervention1" not in st.session_state:
    st.session_state.access_intervention1 = False
if "access_intervention2" not in st.session_state:
    st.session_state.access_intervention2 = False
if "access_intervention3" not in st.session_state:
    st.session_state.access_intervention3 = False

# Access Code Entry for Hidden Page
code1 = get_access_code()  # Get access code from AWS to sync with SMS messaging
code2 = "open-2" #TODO: Change this to another random code from AWS
code3 = "open-3" #TODO: Change this to another random code from AWS


# Sidebar access code entry
with st.sidebar:
    if not (st.session_state.access_intervention1 or st.session_state.access_intervention2 or st.session_state.access_intervention3):
        password = st.text_input("Enter Access Code:", type="password")
        if st.button("Submit"):
            if password == code1:
                st.session_state.access_intervention1 = True
                st.success("Access granted!")
            elif password == code2:
                st.session_state.access_intervention2 = True
                st.success("Access granted!")
            elif password == code3:
                st.session_state.access_intervention3 = True
                st.success("Access granted!")
            else:
                st.error("Incorrect access code.")

    # Display hidden page link if access is granted
    if st.session_state.access_intervention1:
        page_selection = st.radio("Navigate", ["Home", "Low-Frequency Breathing"])
    elif st.session_state.access_intervention2:
        page_selection = st.radio("Navigate", ["Home", "Box Breathing"])
    elif st.session_state.access_intervention3:
        page_selection = st.radio("Navigate", ["Home", "Cyclic Sighing"])
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
    
elif page_selection == "Low-Frequency Breathing" and st.session_state.access_intervention1:
    st.title("Breathwork technique: Low-frequency breathing")
    st.write("Short demonstration video")
    youtube_url = "https://www.youtube.com/watch?v=ZToicYcHIOU"
    st.video(youtube_url)
    st.write("Link in case of technical issues: https://www.youtube.com/watch?v=ZToicYcHIOU")

elif page_selection == "Box Breathing" and st.session_state.access_intervention2:
    st.title("Breathwork technique: Box breathing")
    st.write("Short demonstration video")
    youtube_url = "https://www.youtube.com/watch?v=ZToicYcHIOU"
    st.video(youtube_url)
    st.write("Link in case of technical issues: https://www.youtube.com/watch?v=ZToicYcHIOU")

elif page_selection == "Cyclic Sighing" and st.session_state.access_intervention3:
    st.title("Breathwork technique: Cyclic sighing")
    st.write("Short demonstration video")
    youtube_url = "https://www.youtube.com/watch?v=ZToicYcHIOU"
    st.video(youtube_url)
    st.write("Link in case of technical issues: https://www.youtube.com/watch?v=ZToicYcHIOU")