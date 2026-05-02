# 01 — Local LLM

Call a locally running Ollama model using the OpenAI-compatible API and print the raw request and response.

## Setup

1. Install [Ollama](https://ollama.com) and pull a model:
   ```
   ollama pull gemma4:e4b
   ```

2. Copy the env template and fill in your values:
   ```
   cp .env.example .env
   ```

3. Install dependencies:
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

The script prints the full request JSON, then the full response JSON — every field the API returns including `id`, `model`, `choices`, `usage`, and `finish_reason`.
