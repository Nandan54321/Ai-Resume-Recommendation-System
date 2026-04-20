import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# ---------------------------
# Shared Prompt
# ---------------------------
def build_prompt(query, resume_text):
    return f"""
You are an AI recruiter.

Job Requirement:
{query}

Candidate Resume:
{resume_text}

Return ONLY valid JSON:
{{
  "match_score": number (0-100),
  "matched_skills": [],
  "missing_skills": [],
  "reasoning": ""
}}
"""

# ---------------------------
# Option A: OpenAI
# ---------------------------
def analyze_openai(prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

# ---------------------------
# Option B: Local (Ollama)
# ---------------------------
def analyze_local(prompt):
    url = os.getenv("OLLAMA_URL")
    model = os.getenv("OLLAMA_MODEL")

    response = requests.post(
        f"{url}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

# ---------------------------
# Main Entry
# ---------------------------
def analyze_candidate(query, resume_text):
    prompt = build_prompt(query, resume_text)

    try:
        if LLM_PROVIDER == "local":
            output = analyze_local(prompt)
        else:
            output = analyze_openai(prompt)

        return json.loads(output)

    except Exception as e:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "reasoning": f"LLM failed: {str(e)}"
        }