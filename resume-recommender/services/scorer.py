import os
from openai import OpenAI
from utils.prompt import build_prompt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def score_candidate(job_desc: str, resume_text: str):
    prompt = build_prompt(job_desc, resume_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return eval(response.choices[0].message.content)
    except:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "reason": "Parsing failed"
        }