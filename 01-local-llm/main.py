import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError

load_dotenv()

base_url = os.environ["OLLAMA_BASE_URL"]
model = os.environ["OLLAMA_MODEL"]

input_file = sys.argv[1] if len(sys.argv) > 1 else "request.json"
with open(input_file) as f:
    params = json.load(f)

params["model"] = model

print(f"Sending request to {base_url}/chat/completions (model: {model})")
print()
print("=== REQUEST ===")
print(json.dumps(params, indent=2))
print()

client = OpenAI(base_url=base_url, api_key="ollama", timeout=None)
try:
    response = client.chat.completions.create(**params)
    print("=== RESPONSE ===")
    print(json.dumps(response.model_dump(), indent=2))
except APITimeoutError as e:
    print(f"ERROR: Request timed out — {e}")
    sys.exit(1)
except APIConnectionError as e:
    print(f"ERROR: Could not connect to {base_url} — {e}")
    sys.exit(1)
except APIError as e:
    print(f"ERROR: {e.status_code} {e.message}")
    if e.body:
        print(json.dumps(e.body, indent=2))
    sys.exit(1)
