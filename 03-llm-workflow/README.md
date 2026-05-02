# 03 — LLM Workflow

Classify a directory of `.txt` email files as interesting or uninteresting using a local Ollama model. Uninteresting emails are moved to an `uninteresting/` subfolder, leaving you with only the emails worth reading.

Run multiple passes to progressively narrow down your inbox.

## Setup

1. Copy the env template and fill in your values:
   ```
   cp .env.example .env
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run

```
python main.py <email-dir>
```

Options:
- `--criteria <file>` — criteria file (default: `criteria.txt` in script directory)
- `--dry-run` — classify only, don't move any files

## Criteria file

`criteria.txt` defines what counts as interesting or uninteresting. Edit it to match your preferences. The default covers spam, marketing, class-wide university emails, and personal/job-search emails.

## Output

Each email prints one line:
```
[interesting] email123.txt — personal note from a friend
[uninteresting] email456.txt — spam
```

A timestamped log file (`run_YYYY-MM-DDTHH-MM-SS.log`) is written to the script directory with the full LLM response for every email.
