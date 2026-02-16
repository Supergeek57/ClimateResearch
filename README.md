# ClimateResearch README

Hi! Welcome to my climate research website. This is a simple Streamlit web app to display a demographic intake survey and some breathwork techniques.

## Locations
- Root: Assets and pages for the Streamlit website
- data_cleaning: Scripts for very early data cleaning of weather data from the GHCND database. You shouldn't need to use this unless you are starting the project over from the beginning. Data cleaning steps since Fall 2024 are available in Box/Google Drive (file names are "Data cleaning steps so far", "GIS Steps", and "Stata Steps")

## How to run
- Create a local secrets.toml file and add AWS credentials (see secrets.toml.example)
- pip install streamlit
- streamlit run app.py

## How to deploy in Streamlit Community Cloud
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Note the secrets management step: You will need to save your secrets (AWS API keys) to Streamlit's secrets manager so it can run all the functionality.
