import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_risk(tool_name, data, retries=2):
    prompt = f"""
You are a cybersecurity assistant. Analyze the following {tool_name} result.
Respond in EXACTLY this short format, nothing more:

Risk Level: (Low/Medium/High/Critical)
Summary: (one short sentence, max 15 words)
Recommendation: (one short sentence, max 15 words)

Data:
{data}
"""

    last_error = None
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(1.5)

    return f"AI analysis unavailable after {retries + 1} attempts. Please try again later."