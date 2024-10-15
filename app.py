import streamlit as st
from st_pages import hide_pages
from st_pages import add_page_title, get_nav_from_toml

# Hides interventions in nav bar, but interventions are accessible via the /interventions URL.

home_page = st.Page("home.py", title="Home", icon=":material/home:")
interventions_page = st.Page("interventions.py", title="Interventions", icon=":material/add_circle:")
# delete_page = st.Page("delete.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([home_page, interventions_page], position="hidden")

pg.run()