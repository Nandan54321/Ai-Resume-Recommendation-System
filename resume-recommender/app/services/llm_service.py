# import os
# import json
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

# # ---------------------------
# # Shared Prompt
# # ---------------------------
# def build_prompt(query, resume_text):
#     return f"""
# You are an AI recruiter.

# Job Requirement:
# {query}

# Candidate Resume:
# {resume_text}

# Return ONLY valid JSON:
# {{
#   "match_score": number (0-100),
#   "matched_skills": [],
#   "missing_skills": [],
#   "reasoning": ""
# }}
# """

# # ---------------------------
# # Option A: OpenAI
# # ---------------------------
# def analyze_openai(prompt):
#     from openai import OpenAI
#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2
#     )

#     return response.choices[0].message.content

# # ---------------------------
# # Option B: Local (Ollama)
# # ---------------------------
# def analyze_local(prompt):
#     url = os.getenv("OLLAMA_URL")
#     model = os.getenv("OLLAMA_MODEL")

#     response = requests.post(
#         f"{url}/api/generate",
#         json={
#             "model": model,
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     return response.json()["response"]

# # ---------------------------
# # Main Entry
# # ---------------------------
# def analyze_candidate(query, resume_text):
#     prompt = build_prompt(query, resume_text)

#     try:
#         if LLM_PROVIDER == "local":
#             output = analyze_local(prompt)
#         else:
#             output = analyze_openai(prompt)

#         return json.loads(output)

#     except Exception as e:
#         return {
#             "match_score": 0,
#             "matched_skills": [],
#             "missing_skills": [],
#             "reasoning": f"LLM failed: {str(e)}"
#         }

import json
import requests
from app.core.config import settings


# -----------------------------
# Prompt Builder
# -----------------------------
def build_prompt(query: str, resume_text: str) -> str:
    return f"""
You are an AI recruiter.

Job Requirement:
{query}

Candidate Resume:
{resume_text}

Analyze the candidate and return ONLY valid JSON:

{{
  "match_score": number (0-100),
  "matched_skills": [],
  "missing_skills": [],
  "reasoning": ""
}}

Rules:
- Be strict and realistic in scoring
- Match skills explicitly mentioned
- Keep reasoning short (1-2 lines)
"""
    

# -----------------------------
# OpenAI (Option A)
# -----------------------------
def analyze_with_openai(prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# -----------------------------
# Local Model (Option B - Ollama)
# -----------------------------
def analyze_with_local(prompt: str) -> str:
    response = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )

    response.raise_for_status()
    return response.json().get("response", "")


# -----------------------------
# JSON Parser (robust)
# -----------------------------
def safe_parse_llm_output(output: str) -> dict:
    try:
        # Try direct JSON parse
        return json.loads(output)
    except:
        try:
            # Try to extract JSON from messy output
            start = output.find("{")
            end = output.rfind("}") + 1
            return json.loads(output[start:end])
        except:
            return {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "reasoning": "Failed to parse LLM response"
            }


# -----------------------------
# Main Entry Function
# -----------------------------
def analyze_candidate(query: str, resume_text: str) -> dict:
    prompt = build_prompt(query, resume_text)

    try:
        if settings.LLM_PROVIDER == "local":
            raw_output = analyze_with_local(prompt)
        else:
            raw_output = analyze_with_openai(prompt)

        parsed = safe_parse_llm_output(raw_output)

        # Ensure required fields exist
        return {
            "match_score": int(parsed.get("match_score", 0)),
            "matched_skills": parsed.get("matched_skills", []),
            "missing_skills": parsed.get("missing_skills", []),
            "reasoning": parsed.get("reasoning", "")
        }

    except Exception as e:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "reasoning": f"LLM error: {str(e)}"
        }