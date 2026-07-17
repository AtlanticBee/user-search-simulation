import urllib.request
import urllib.error
import json

def get_llm_response(query, description="a user"):

    base_url = "http://localhost:11434/api/chat"

    request_body = {
        "model":"phi4-mini",
        # Note it could receive multiple messages at once - but this is to keep a timeline of a single conversation, not for batch processing.
        "messages": [
            {
                "role": "system",
                "content": "You are a direct conversational assistant. Do NOT use any thinking tags, do not output internal reasoning, and do not write or invent subsequent instructions. Respond only with the immediate conversational answer."
            },
            {
                "role":"user",
                "content":query
            }
        ],
        "stream":False,     # We're not sending over characters as they're typed.
        "think": False,     # This tells it to return just the reply, not the "thought" behind it.
        "options": {
            "temperature":0.2,      # Measure of how random the LLM response is.
            # "num_predict":12        # An length limit for the response in tokens (approx 4 chars in English)
        }
    }

    payload = json.dumps(request_body).encode('utf-8')

    req = urllib.request.Request(
        base_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        print(f"Sending query for {description}...")
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_body = response.read().decode("utf-8")
            result = json.loads(raw_body)

            # Chat API nests strings under message -> content
            model_response = result.get('message', {})
            clean_query = model_response.get('content','').strip()

            return clean_query

    except urllib.error.URLError as e:
        print(f"\n[ERROR] Connection failed: {e.reason}")