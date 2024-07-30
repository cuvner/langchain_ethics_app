import pandas as pd

def create_detailed_dataframe(submissions):
    detailed_submissions = []
    max_considerations = 0

    # Determine the maximum number of ethical considerations
    for submission in submissions:
        max_considerations = max(max_considerations, len(submission['ethical_considerations']))

    for submission in submissions:
        detailed_submission = {
            "Title": submission['title'],
            "Methods": "; ".join(submission['research_methods']),
            "Overall Risk": submission['risk_level']
        }
        for i in range(max_considerations):
            if i < len(submission['ethical_considerations']):
                detailed_submission[f"Ethical Consideration {i+1}"] = submission['ethical_considerations'][i]
            else:
                detailed_submission[f"Ethical Consideration {i+1}"] = ""

        detailed_submissions.append(detailed_submission)

    df = pd.DataFrame(detailed_submissions)
    return df
