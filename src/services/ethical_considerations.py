import pandas as pd

def create_detailed_dataframe(submissions):
    detailed_submissions = []
    for submission in submissions:
        for method, consideration in zip(submission['research_methods'], submission['ethical_considerations']):
            detailed_submissions.append({
                "Title": submission['title'],
                "Risk Level": submission['risk_level'],
                "Method": method,
                "Ethical Consideration": consideration,
            })
    df = pd.DataFrame(detailed_submissions)
    return df

