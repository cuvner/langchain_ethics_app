import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from src.config import get_openai_api_key

# Define prompt templates
prompt1 = ChatPromptTemplate.from_template("Based on the description '{description}', what are the potential risks associated with this research project that {participant_clause}? Please return just one risk assessment.")
prompt2 = ChatPromptTemplate.from_template("Given the description '{description}' and the methods: {research_methods}, what would be an effective study design for a research project that {participant_clause} with participants who are {age_clause}? Please include considerations for how to implement these methods effectively and ethically.")

def load_methods(file_path='src/methods.txt'):
    with open(file_path, 'r') as file:
        methods = [line.strip() for line in file if line.strip()]
    return methods

def save_new_method(method, file_path='src/methods.txt'):
    with open(file_path, 'a') as file:
        file.write(f"\n{method}")

def design_methods_page():
    st.title('Generate appropriate research methods')

    st.write("""
    This page helps generate your research methods. Follow the steps below to get started:
    """)

    # Step 1: Description of the Study and Research Questions
    st.header("Step 1: Description of the Study and Research Questions")
    description = st.text_area("Enter the description of your study and the research questions", height=200)

    # Step 2: Select Your Research Methods
    st.header("Step 2: Select Your Research Methods")
    methods = load_methods()
    selected_methods = st.multiselect("Choose the methods you plan to use", methods)

    # Option to add a new method
    st.subheader("Add a new method if it's not listed")
    new_method = st.text_input("New Method")
    if st.button("Add Method"):
        if new_method and new_method not in methods:
            save_new_method(new_method)
            methods.append(new_method)
            st.success(f"Method '{new_method}' added. Please re-select your methods.")
        else:
            st.error("Please enter a valid new method that is not already listed.")

    # Step 3: Specify Participant Details
    st.header("Step 3: Specify Participant Details")
    uses_participants = st.radio("Does the research use participants?", ("Yes", "No")) == "Yes"
    participants_over_18 = None
    if uses_participants:
        participants_over_18 = st.radio("Are participants over 18?", ("Yes", "No")) == "Yes"

    # Step 4: Generate Study Design
    st.header("Step 4: Generate Study Design")
    if st.button("Generate Study Design"):
        if not description or not selected_methods:
            st.error("Please enter a study description and select at least one method.")
        else:
            openapi_key = get_openai_api_key()
            try:
                with st.spinner('Generating study design...'):
                    participant_clause = "uses participants" if uses_participants else "does not use participants"
                    age_clause = "over 18" if participants_over_18 else "under 18"
                    research_methods = ", ".join(selected_methods)

                    # Create a ChatOpenAI model
                    model = ChatOpenAI(model="gpt-4", openai_api_key=openapi_key)

                    # Create chains
                    chain1 = prompt1 | model | StrOutputParser()
                    chain2 = prompt2 | model | StrOutputParser()

                    # Get risk assessment
                    risk_response = chain1.invoke({"description": description, "participant_clause": participant_clause})
                    risk = risk_response.strip()

                    # Generate study design
                    study_design_response = chain2.invoke({
                        "description": description,
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
