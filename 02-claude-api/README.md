# 02 — Claude API

Call Claude using the Anthropic SDK and print the raw request and response.

Note how the request format differs from exercise 01: the system prompt is a top-level field (not a message), and messages only contain user/assistant turns.

## Setup

1. Get an API key from [console.anthropic.com](https://console.anthropic.com)

2. Copy the env template and fill in your key:
   ```
   cp .env.example .env
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run

```
python main.py
```

Or pass a custom request file:

```
python main.py my_request.json
```

## What you'll see

The script prints the full request JSON, then the full response JSON — every field the API returns including `id`, `model`, `content`, `usage`, and `stop_reason`.
