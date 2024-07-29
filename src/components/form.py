import streamlit as st

def display_form():
    title = st.text_input("Enter the research title")
    uses_participants = st.radio("Does the research use participants?", ("Yes", "No"))
    participants_over_18 = st.radio("Are participants over 18?", ("Yes", "No"))
    research_methods = st.text_area("Describe the research methods")
    return title, uses_participants, participants_over_18, research_methods

