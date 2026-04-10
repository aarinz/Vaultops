import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_model(prompt: str) -> str:
    try:
        response = requests.post(API_URL, headers=headers, json={
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.3
        }, timeout=60)
        if response.status_code != 200:
            return f"AI engine error: {response.status_code} {response.text}"
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
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
    pre_rate = pre_metrics.get("transaction_success_rate", 0)
    post_rate = post_metrics.get("transaction_success_rate", 0)

    drop = pre_rate - post_rate

    if drop > 1.0:
        return {
            "should_rollback": True,
            "reason": f"Transaction success rate decreased by {drop:.1f}%"
        }

    return {
        "should_rollback": False,
        "reason": f"Metrics stable. Drop = {drop:.1f}%"
    }