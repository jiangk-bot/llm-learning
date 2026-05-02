import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError

SCRIPT_DIR = Path(__file__).parent

SYSTEM_PROMPT = (
    "You are an email classifier. Classify emails as interesting or uninteresting "
    "based on the provided criteria. Respond with valid JSON only, using this exact format: "
    '{"decision": "interesting" or "uninteresting", "rationale": "brief explanation of 30 words or less — be concise, e.g. just \'spam\' for obvious spam"}'
)


def build_user_prompt(criteria: str, email_content: str) -> str:
    return f"Criteria:\n{criteria}\n\nEmail:\n{email_content}"


def classify_email(client, model, criteria, email_content, max_chars):
    truncated = email_content[:max_chars]
    user_prompt = build_user_prompt(criteria, truncated)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    raw = response.model_dump()
    text = response.choices[0].message.content

    try:
        parsed = json.loads(text)
        decision = parsed.get("decision", "").lower()
        rationale = parsed.get("rationale", "")
        if decision not in ("interesting", "uninteresting"):
            raise ValueError(f"Unexpected decision value: {decision!r}")
        return decision, rationale, raw, None
    except Exception as e:
        return "interesting", "(parse error — defaulting to interesting)", raw, str(e)


def main():
    load_dotenv(SCRIPT_DIR / ".env")

    base_url = os.environ["OLLAMA_BASE_URL"]
    model = os.environ["OLLAMA_MODEL"]
    max_chars = int(os.environ.get("MAX_CHARS", 8000))

    parser = argparse.ArgumentParser(description="Classify emails as interesting or uninteresting.")
    parser.add_argument("email_dir", help="Directory containing .txt email files")
    parser.add_argument("--criteria", default=str(SCRIPT_DIR / "criteria.txt"), help="Path to criteria file")
    parser.add_argument("--dry-run", action="store_true", help="Classify only, do not move files")
    args = parser.parse_args()

    email_dir = Path(args.email_dir)
    if not email_dir.is_dir():
        print(f"ERROR: {email_dir} is not a directory")
        sys.exit(1)

    criteria_path = Path(args.criteria)
    if not criteria_path.exists():
        print(f"ERROR: Criteria file not found: {criteria_path}")
        sys.exit(1)
    criteria = criteria_path.read_text()

    uninteresting_dir = email_dir / "uninteresting"
    if not args.dry_run:
        uninteresting_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    log_path = SCRIPT_DIR / f"run_{timestamp}.log"

    email_files = sorted(f for f in email_dir.glob("*.txt"))
    if not email_files:
        print("No .txt files found.")
        sys.exit(0)

    dry_run_label = " [DRY RUN]" if args.dry_run else ""
    print(f"Classifying {len(email_files)} emails using {model}{dry_run_label}")
    print(f"Log: {log_path}")
    print()

    client = OpenAI(base_url=base_url, api_key="ollama", timeout=None)

    interesting_count = 0
    uninteresting_count = 0

    with open(log_path, "w") as log_file:
        for email_file in email_files:
            try:
                email_content = email_file.read_text(errors="replace")
            except Exception as e:
                print(f"[error] {email_file.name} — could not read file: {e}")
                continue

            try:
                decision, rationale, raw_response, parse_error = classify_email(
                    client, model, criteria, email_content, max_chars
                )
            except (APITimeoutError, APIConnectionError, APIError) as e:
                print(f"[error] {email_file.name} — API error: {e}")
                log_file.write(json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "file": email_file.name,
                    "decision": "error",
                    "rationale": str(e),
                    "raw_response": None,
                }) + "\n")
                continue

            print(f"[{decision}] {email_file.name} — {rationale}")

            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "file": email_file.name,
                "decision": decision,
                "rationale": rationale,
                "raw_response": raw_response,
            }
            if parse_error:
                log_entry["parse_error"] = parse_error
            log_file.write(json.dumps(log_entry) + "\n")

            if decision == "uninteresting":
                uninteresting_count += 1
                if not args.dry_run:
                    shutil.move(str(email_file), str(uninteresting_dir / email_file.name))
            else:
                interesting_count += 1

    print()
    moved_label = "would move" if args.dry_run else "moved"
    print(f"Done: {interesting_count} interesting, {uninteresting_count} {moved_label} to uninteresting/")


if __name__ == "__main__":
    main()
