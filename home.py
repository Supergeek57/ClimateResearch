import streamlit as st
from st_pages import hide_pages
from st_pages import add_page_title, get_nav_from_toml
import streamlit.components.v1 as components

st.write("# Survey")
st.write("This survey will help us understand your background and current subjective mood. It should only take about 5 minutes to complete.")

survey_url = "https://universityofalabama.az1.qualtrics.com/jfe/form/SV_6gnRQdY0zIUMtUO"
iframe_code = f'<iframe src="{survey_url}" height="800px" width="600px"></iframe>'

# Display the iframe in the Streamlit app
components.html(iframe_code, height=800, width=600)