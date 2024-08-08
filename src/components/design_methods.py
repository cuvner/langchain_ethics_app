import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from src.config import get_openai_api_key

# Define prompt templates
prompt1 = ChatPromptTemplate.from_template("What are the risks associated with a research project titled '{title}' that {participant_clause}? Please return just one risk assessment.")
prompt2 = ChatPromptTemplate.from_template("What would be a good study design for a research project titled '{title}' that {participant_clause} with participants who are {age_clause}? The research methods are: {research_methods}")

def design_methods_page():
    st.title('Research Study Design')

    st.write("""
    This page helps you design your research methods. Follow the steps below to get started:
    """)

    # Step 1: Define Your Research Questions
    st.header("Step 1: Define Your Research Questions")
    title = st.text_input("Enter your main research question")

    # Step 2: Select Your Research Methods
    st.header("Step 2: Select Your Research Methods")
    methods = st.multiselect(
        "Choose the methods you plan to use",
        ["Surveys", "Interviews", "Focus Groups", "Observations", "Experiments", "Case Studies"]
    )

    # Step 3: Specify Participant Details
    st.header("Step 3: Specify Participant Details")
    uses_participants = st.radio("Does the research use participants?", ("Yes", "No")) == "Yes"
    participants_over_18 = None
    if uses_participants:
        participants_over_18 = st.radio("Are participants over 18?", ("Yes", "No")) == "Yes"

    # Step 4: Generate Study Design
    st.header("Step 4: Generate Study Design")
    if st.button("Generate Study Design"):
        if not title or not methods:
            st.error("Please enter a research title and select at least one method.")
        else:
            openapi_key = get_openai_api_key()
            try:
                with st.spinner('Generating study design...'):
                    participant_clause = "uses participants" if uses_participants else "does not use participants"
                    age_clause = "over 18" if participants_over_18 else "under 18"
                    research_methods = ", ".join(methods)

                    # Create a ChatOpenAI model
                    model = ChatOpenAI(model="gpt-4", openai_api_key=openapi_key)

                    # Create chains
                    chain1 = prompt1 | model | StrOutputParser()
                    chain2 = prompt2 | model | StrOutputParser()

                    # Get risk assessment
                    risk_response = chain1.invoke({"title": title, "participant_clause": participant_clause})
                    risk = risk_response.strip()

                    # Generate study design
                    study_design_response = chain2.invoke({
                        "title": title,
                        "participant_clause": participant_clause,
                        "age_clause": age_clause,
                        "research_methods": research_methods
                    })
                    study_design = study_design_response.strip()

                    st.success('Study design generated successfully!')
                    st.subheader("Risk Assessment")
                    st.write(risk)
                    st.subheader("Study Design")
                    st.write(study_design)

            except Exception as e:
                st.error(f"Error generating study design: {e}")
