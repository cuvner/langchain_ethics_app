import streamlit as st

def get_openai_api_key():
    try:
        openapi_key = st.secrets["openapi_key"]
        return openapi_key
    except KeyError:
        st.error("The OpenAI API key is not set. Please add your OpenAI API key to the Streamlit secrets.")
        st.stop()

