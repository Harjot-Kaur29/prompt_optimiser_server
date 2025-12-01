import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = os.getenv("GROQ_API_URL")
MODEL = os.getenv("GROQ_MODEL")


def analyse_prompt(user_prompt: str) -> dict:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a highly experienced prompt engineer with 20 years of expertise in creating high-quality prompts.\n\n"
                "Your task: Analyze the user’s prompt and respond ONLY in valid JSON, matching exactly this schema:\n"
                "{\n"
                "  \"summary\": \"string\",\n"
                "  \"issues\": [\"string\"],\n"
                "  \"suggestions\": [\"string\"],\n"
                "  \"optimized_prompt\": \"string\",\n"
                "  \"raw_text\": \"string\"\n"
                "}\n\n"
                "STRICT RULES:\n"
                "• Respond with ONLY the JSON object — no extra text, no labels, no explanation.\n"
                "• Do NOT wrap the output in markdown formatting like ```json or ```.\n"
                "• Do NOT include comments.\n"
                "• Use double quotes for all strings.\n"
                "• Include ALL keys even if empty (use \"\" or []).\n"
                "• JSON must be fully valid and parsable.\n"
                "• The \"optimized_prompt\" must be an improved, clearer version of the user's prompt, ready for direct use.\n"
            ),
        },
        {
            "role": "user",
            "content": f'Here is the prompt to analyze:\n"""{user_prompt}"""',
        },
    ]

    if not API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    body = {
        "model": MODEL,
        "messages": messages,
    }

    # API call
    resp = requests.post(API_URL, headers=headers, json=body)
    resp.raise_for_status()

    data = resp.json()

    if "error" in data:
        raise RuntimeError(f"Groq API error: {data['error']}")

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected LLM response format: {data}")

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "summary": "",
            "issues": ["Model did not return valid JSON. Please try again later.."],
            "suggestions": [],
            "optimized_prompt": "",
            "raw_text": content,
        }

    return parsed
