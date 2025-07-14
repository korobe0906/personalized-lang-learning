import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-70b-8192"  # hoặc mixtral...

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing! Kiểm tra lại file .env")

def get_response(prompt, model=GROQ_MODEL):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP error:", e)
        print("📄 Response text:", res.text)
        raise
    except Exception as e:
        print("❌ Other error:", e)
        raise
