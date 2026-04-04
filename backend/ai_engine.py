import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_model(prompt: str) -> str:
    try:
        response = requests.post(API_URL, headers=headers, json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 512, "temperature": 0.3, "return_full_text": False}
        }, timeout=60)
        result = response.json()
        if isinstance(result, list):
            return result[0]["generated_text"].strip()
        return str(result)
    except Exception as e:
        return f"AI engine error: {str(e)}"

def analyze_risk(description: str) -> dict:
    prompt = f"""[INST] You are a fintech business analyst AI. Analyze this software release and return ONLY a JSON object with these exact keys:
- risk_score: integer 0-100 (100 = highest risk)
- reasoning: string explaining the score
- regulatory_flags: list of strings (PCI-DSS or SOX violations found, empty list if none)
- recommendation: string (approve or reject)

Release description: {description}

Return ONLY valid JSON, no extra text. [/INST]"""
    
    raw = query_model(prompt)
    
    import json, re
    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    
    return {
        "risk_score": 50,
        "reasoning": raw,
        "regulatory_flags": [],
        "recommendation": "review"
    }

def analyze_rollback(pre_metrics: dict, post_metrics: dict) -> dict:
    prompt = f"""[INST] You are a fintech DevOps BA. Compare these metrics and return ONLY a JSON object:
- should_rollback: boolean
- reason: string

Pre-deploy metrics: {pre_metrics}
Post-deploy metrics: {post_metrics}

Return ONLY valid JSON. [/INST]"""
    
    raw = query_model(prompt)
    
    import json, re
    try:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    
    return {"should_rollback": False, "reason": raw}