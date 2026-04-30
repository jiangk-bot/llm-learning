# LLM Learning Progression

A series of Python examples that build up from a basic local LLM call to a full agentic workflow.

## Prerequisites

- [Ollama](https://ollama.com) installed and running locally
- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com) (for examples 2+)

## Examples

### 1. Local LLM (`01-local-llm/`)

Call a locally running model via Ollama and print the response. Covers:
- Sending a prompt to a local model over HTTP
- Reading and printing the response

### 2. Claude API (`02-claude-api/`)

Call Claude using the Anthropic Python SDK and print the response. Covers:
- Installing and using the `anthropic` SDK
- API key authentication
- Basic request/response structure

### 3. LLM Workflow (`03-llm-workflow/`)

Chain multiple LLM calls together to accomplish a multi-step task. Covers:
- Passing context between calls
- Prompt chaining and composition
- Structured output (e.g. JSON)

### 4. Agentic LLM (`04-agentic-llm/`)

Give the model tools and let it reason through a task autonomously. Covers:
- Tool/function definitions
- The tool-use loop (model calls tool → tool runs → result fed back)
- Multi-step autonomous decision-making

## Running the Examples

Each folder contains its own `README.md` with setup and run instructions.
