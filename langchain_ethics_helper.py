from secret_key import openapi_key
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
import os

# Load environment variables from .env
os.environ["OPENAI_API_KEY"] = openapi_key

# Define prompt templates
prompt1 = ChatPromptTemplate.from_template("What are the risks associated with a research project titled '{title}' that {participant_clause}? Please return just one risk assessment.")
prompt2 = ChatPromptTemplate.from_template("What sections are required for the ethical form of a research project titled '{title}' that {participant_clause}?")

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4")

# Create chains
chain1 = prompt1 | model | StrOutputParser()
chain2 = prompt2 | model | StrOutputParser()

# Function to invoke the chain
def ethics_application_function(title, uses_participants):
    if not isinstance(title, str):
        raise TypeError("Expected title to be a string.")
    if not isinstance(uses_participants, bool):
        raise TypeError("Expected uses_participants to be a boolean.")

    participant_clause = "uses participants" if uses_participants else "does not use participants"
    
    # Get risk assessment
    risk_response = chain1.invoke({"title": title, "participant_clause": participant_clause})
    risk = risk_response.strip()

    # Generate required sections
    sections_response = chain2.invoke({"title": title, "participant_clause": participant_clause})
    sections = sections_response.strip()

    return {"risk": risk, "sections": sections}

# Example usage
if __name__ == "__main__":
    title_input = "Study on the Effects of Social Media on Teenagers"  # Ensure the input is a string
    uses_participants_input = True  # Ensure the input is a boolean

    response = ethics_application_function(title_input, uses_participants_input)
    print("Risk Assessment:", response['risk'])
    print("Required Sections:", response['sections'])
