import json
import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()

model = os.environ["ANTHROPIC_MODEL"]

input_file = sys.argv[1] if len(sys.argv) > 1 else "request.json"
with open(input_file) as f:
    params = json.load(f)

params["model"] = model

print(f"Sending request to api.anthropic.com (model: {model})")
print()
print("=== REQUEST ===")
print(json.dumps(params, indent=2))
print()

client = anthropic.Anthropic()
try:
    response = client.messages.create(**params)
    print("=== RESPONSE ===")
    print(json.dumps(response.model_dump(), indent=2))
except anthropic.APITimeoutError as e:
    print(f"ERROR: Request timed out — {e}")
    sys.exit(1)
except anthropic.APIConnectionError as e:
    print(f"ERROR: Could not connect to api.anthropic.com — {e}")
    sys.exit(1)
except anthropic.APIError as e:
    print(f"ERROR: {e.status_code} {e.message}")
    if e.body:
        print(json.dumps(e.body, indent=2))
    sys.exit(1)
