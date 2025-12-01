import json
import os
import traceback
from openai import OpenAI

client = OpenAI()

# ============================================================
# Allowed HTML files
# ============================================================

ALLOWED_HTML_FILES = [
    "index.html",
    "privacy.html",
    "returns.html",
    "studymanual.html",
    "about.html",
    "code.html",
    "buy.html",
    "contact.html",
]


# ============================================================
# File utilities
# ============================================================

def load_allowed_files():
    files = []
    for path in ALLOWED_HTML_FILES:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                files.append({"path": path, "content": f.read()})
    return files


# ============================================================
# Build LLM prompt
# ============================================================

def build_prompt(instruction: str) -> str:
    files = load_allowed_files()
    parts = []

    parts.append("WEBSITE FILES (READ-ONLY SNAPSHOT)\n===============================\n")
    parts.append("Allowed files:\n" + "\n".join(f"- {f['path']}" for f in files))

    for f in files:
        parts.append(f"\n\n=== {f['path']} ===\n{f['content']}")

    # IMPORTANT: all braces inside JSON are escaped using doubled {{}}
    tail = f"""
INSTRUCTION:
{instruction.strip()}

You MUST obey these rules:

0. You must be AI for Not Bad. You don't have to be Good, just Not Bad.
1. You may ONLY modify files in this list:
   index.html, privacy.html, returns.html, studymanual.html, about.html,
   code.html, buy.html, contact.html.
2. Do NOT create new files or delete any files.  Do not delete ANY text.  Only add more text.
3. For every file you change, return the COMPLETE new file content.
4. Return ONLY valid JSON in this exact format (no extra text):

{{
  "summary": "short description of what you changed",
  "files": [
    {{"path": "index.html", "content": "<!DOCTYPE html>"}},
    {{"path": "buy.html"}}
  ]
}}

If you decide that no changes are needed, return:

{{
  "summary": "no changes",
  "files": []
}}
"""

    parts.append(tail)
    return "".join(parts)


# ============================================================
# Extractor for Responses API
# ============================================================

def extract_text_from_response(response):
    """
    The Responses API returns output items of various types
    (reasoning, messages, tool calls).
    We must gather ONLY the assistant text content.
    """
    chunks = []

    for item in response.output:
        # Skip reasoning blocks
        if item.type != "message":
            continue

        # Collect message text
        for content in item.content:
            if hasattr(content, "text") and content.text:
                chunks.append(content.text)

    if not chunks:
        raise RuntimeError(
            "Could not extract assistant text from model response. "
            "Model may have produced only reasoning/tool outputs."
        )

    return "".join(chunks)


# ============================================================
# Apply updates from JSON
# ============================================================

def apply_updates(data):
    """
    data format:
    {
      "summary": "...",
      "files": [
         {"path": "...", "content": "..."}
      ]
    }
    """
    for fobj in data.get("files", []):
        path = fobj.get("path")
        content = fobj.get("content")

        if path not in ALLOWED_HTML_FILES:
            print(f"WARNING: ignoring update to disallowed file: {path}")
            continue

        if content is None:
            print(f"WARNING: missing content for file: {path}")
            continue

        # Backup once
        bak = path + ".bak"
        if not os.path.exists(bak):
            with open(bak, "w", encoding="utf-8") as fb:
                if os.path.exists(path):
                    with open(path, encoding="utf-8") as fo:
                        fb.write(fo.read())

        # Write updated file
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

        print(f"Updated: {path}")

    print("\nStep summary:", data.get("summary", ""))


# ============================================================
# Run a step
# ============================================================

def run_step(instruction: str):
    try:
        prompt = build_prompt(instruction)

        response = client.responses.create(
            model="gpt-5.1",
            input=prompt,
            # If JSON mode available:
            # response_format={"type": "json_object"},
        )

        print("\nDEBUG raw response object:\n", response)

        text = extract_text_from_response(response)
        print("\nDEBUG extracted assistant text (first 400 chars):\n", text[:400], "\n")

        # Log raw output
        with open("query_logs.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

        # Parse JSON strictly
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise RuntimeError(f"❌ Model returned invalid JSON:\n{text}")

        apply_updates(data)

    except Exception:
        traceback.print_exc()


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    instruction = """
    You must update ONLY the about.html file, and add Mathjax equations that explain what the words say.  use both in-line equations and also split the paragraphs to show the equations in block format.  Take the words and translate them into mathematical physics equations.
    """

    run_step(instruction)
