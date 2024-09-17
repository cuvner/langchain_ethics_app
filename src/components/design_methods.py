import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from src.config import get_openai_api_key

# Define the prompt template for generating research methods
prompt1 = ChatPromptTemplate.from_template("Based on the research project titled '{title}' and the following research questions: '{description}', what are the most appropriate research methods that should be considered for this study? Please provide a concise list of methods.")

def design_methods_page():
    st.title('Develop Your Research Methods')

    # Use unique keys for this page to avoid conflicts with other pages like the ethics page
    if 'research_title' not in st.session_state:
        st.session_state.research_title = ""
    if 'research_description' not in st.session_state:
        st.session_state.research_description = ""
    if 'advised_methods' not in st.session_state:
        st.session_state.advised_methods = ""

    st.write("""
    This page will help you generate appropriate research methods based on your research title and research questions.
    Please provide the information below to receive your advised methods:
    """)

    # Research Title
    st.header("Research Title")
    research_title = st.text_input("Enter the title of your research", value=st.session_state.research_title)

    # Research Questions
    st.header("Research Questions")
    research_description = st.text_area("Enter the research questions or a description of the study", height=200, value=st.session_state.research_description)

    # Save the title and description to session state when the inputs change
    st.session_state.research_title = research_title
    st.session_state.research_description = research_description

    # Generate Advised Research Methods
    if st.button("Generate Advised Research Methods"):
        # Validation for required inputs
        if not research_title:
            st.error("Please enter the research title.")
        elif not research_description:
            st.error("Please enter the research questions or a description of the study.")
        else:
            openapi_key = get_openai_api_key()
            try:
                with st.spinner('Generating research methods...'):
                    # Create a ChatOpenAI model
                    model = ChatOpenAI(model="gpt-4", openai_api_key=openapi_key)

                    # Create chain for generating research methods
                    chain1 = prompt1 | model | StrOutputParser()

                    # Get advised research methods
                    methods_response = chain1.invoke({
                        "title": research_title,
                        "description": research_description
                    })
                    advised_methods = methods_response.strip()

                    # Store the advised methods in session state
                    st.session_state.advised_methods = advised_methods

                    st.success('Advised research methods generated successfully!')
                    st.subheader("Advised Research Methods")
                    st.write(advised_methods)

            except Exception as e:
                st.error(f"Error generating advised research methods: {e}")

    # Display previously generated methods if they exist
    if st.session_state.advised_methods:
        st.subheader("Previously Generated Advised Research Methods")
        st.write(st.session_state.advised_methods)
