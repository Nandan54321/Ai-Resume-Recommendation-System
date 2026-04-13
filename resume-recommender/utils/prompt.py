def build_prompt(job: str, resume: str):
    return f"""
You are a recruitment AI.

Job Description:
{job}

Candidate Resume:
{resume}

Evaluate:
1. Match Score (0–100)
2. Matched Skills
3. Missing Skills
4. Reasoning (2–3 lines)

Return JSON format:
{{
  "score": int,
  "matched_skills": [],
  "missing_skills": [],
  "reason": ""
}}
"""