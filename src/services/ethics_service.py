from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

# Define prompt templates
prompt1 = ChatPromptTemplate.from_template("What are the ethical issues associated with a research project titled '{title}' that {participant_clause}? Please return just one risk assessment.")
prompt2 = ChatPromptTemplate.from_template("What are the ethical issues related to the following research methods involving {age_clause}: {research_methods}? Please focus on ethical issues and how to address them.")
prompt3 = ChatPromptTemplate.from_template("Based on the following research methods involving {age_clause}, assess the risk level of the research project titled '{title}'. The methods are: {research_methods}. Please categorize the risk level as Low, Medium, or High and provide a brief explanation.")

# Function to invoke the chain
def ethics_application_function(title, uses_participants, participants_over_18, research_methods, openapi_key):
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
    
    try:
        # Create a ChatOpenAI model
        model = ChatOpenAI(model="gpt-4", openai_api_key=openapi_key)

        # Create chains
        chain1 = prompt1 | model | StrOutputParser()
        chain2 = prompt2 | model | StrOutputParser()
        chain3 = prompt3 | model | StrOutputParser()
        
        # Get risk assessment
        risk_response = chain1.invoke({"title": title, "participant_clause": participant_clause})
        risk = risk_response.strip()

        # Generate study design focusing on ethical issues
        study_design_response = chain2.invoke({
            "title": title,
            "participant_clause": participant_clause,
            "age_clause": age_clause,
            "research_methods": research_methods
        })
        study_design = study_design_response.strip()

        # Assess risk level
        risk_level_response = chain3.invoke({
            "title": title,
            "participant_clause": participant_clause,
            "age_clause": age_clause,
            "research_methods": research_methods
        })
        risk_level = risk_level_response.strip()

        return {"risk": risk, "study_design": study_design, "risk_level": risk_level}
    
    except Exception as e:
        raise RuntimeError(f"Error generating ethics application: {e}")
