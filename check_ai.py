import os
import requests

url = os.environ["LLM_BASE_URL"].rstrip("/") + "/chat/completions"

response = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {os.environ['LLM_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": os.environ["LLM_MODEL"],
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly: AI connection successful"
            }
        ],
    },
    timeout=60,
)

print("HTTP status:", response.status_code)
response.raise_for_status()
print(response.json()["choices"][0]["message"]["content"])