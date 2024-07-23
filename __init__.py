from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Now you can access the OPENAI_API_KEY environment variable
openapi_key = os.getenv("OPENAI_API_KEY")

# Define prompt templates
prompt1 = ChatPromptTemplate.from_template("What are the risks associated with a research project titled '{title}' that {participant_clause}? Please return just one risk assessment.")
prompt2 = ChatPromptTemplate.from_template("What would be a good study design for a research project titled '{title}' that {participant_clause} with participants who are {age_clause}? The research methods are: {research_methods}")

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4")

# Create chains
chain1 = prompt1 | model | StrOutputParser()
chain2 = prompt2 | model | StrOutputParser()

# Function to invoke the chain
def ethics_application_function(title, uses_participants, participants_over_18, research_methods):
    if not isinstance(title, str):
        raise TypeError("Expected title to be a string.")
    if not isinstance(uses_participants, bool):
        raise TypeError("Expected uses_participants to be a boolean.")
    if not isinstance(participants_over_18, bool):
        raise TypeError("Expected participants_over_18 to be a boolean.")
    if not isinstance(research_methods, str):
        raise TypeError("Expected research_methods to be a string.")

    participant_clause = "uses participants" if uses_participants else "does not use participants"
    age_clause = "over 18" if participants_over_18 else "under 18"
    
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

    return {"risk": risk, "study_design": study_design}
