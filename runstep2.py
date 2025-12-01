import json
import os
import traceback
from openai import OpenAI

client = OpenAI()

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

def load_allowed_files():
    files = []
    for path in ALLOWED_HTML_FILES:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                files.append({"path": path, "content": f.read()})
    return files

def build_prompt(instruction: str) -> str:
    files = load_allowed_files()
    parts = []

    parts.append("WEBSITE FILES (READ-ONLY SNAPSHOT)\n===============================\n")
    parts.append("Allowed files:\n" + "\n".join(f"- {f['path']}" for f in files))

    for f in files:
        parts.append(f"\n\n=== {f['path']} ===\n{f['content']}")

    tail = """
INSTRUCTION:
{instruction}

You MUST obey these rules:

1. You may ONLY modify files in this list:
   index.html, privacy.html, returns.html, studymanual.html, about.html, code.html, buy.html, contact.html.
2. Do NOT create new files or delete any files.
3. For every file you change, return the COMPLETE new file content.
4. Return ONLY valid JSON in this exact format (no extra text):

{
  "summary": "short description of what you changed",
  "files": [
    {"path": "index.html", "content": "<!DOCTYPE html>..."},
    {"path": "buy.html", "content": "..."}
  ]
}

If you decide that no changes are needed, return:

{
  "summary": "no changes",
  "files": []
}
""".format(instruction=instruction.strip())

    parts.append(tail)
    return "".join(parts)

def run_step(instruction: str):
    try:
        prompt = build_prompt(instruction)

        response = client.responses.create(
            model="gpt-5",
            input=prompt,
            # if your account supports it, you can enforce JSON:
            # response_format={"type": "json_object"},
        )

        # DEBUG: see the raw object once to confirm structure
        print("DEBUG raw response:", response)

        # Adjust this line to however your SDK exposes text.
        # For many recent responses-style calls, the text is here:
        text = response.output[0].content[0].text

        print("DEBUG text snippet:", text[:400])

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            print("JSON error:", e)
            print("Raw text:\n", text)
            return

        # Log full JSON to a query log
        with open("query_logs.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

        # Apply only allowed file updates
        for fobj in data.get("files", []):
            path = fobj.get("path")
            content = fobj.get("content")
            if path not in ALLOWED_HTML_FILES or content is None:
                print("Ignoring unexpected file entry:", fobj)
                continue

            # One-time backup
            bak = path + ".bak"
            if not os.path.exists(bak) and os.path.exists(path):
                with open(bak, "w", encoding="utf-8") as fb:
                    with open(path, encoding="utf-8") as fo:
                        fb.write(fo.read())

            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)

            print(f"Updated: {path}")

        print("Step summary:", data.get("summary", ""))

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    instruction = """
    1. In index.html, change the <title> to "Predictive Insights".
    2. In any HTML files that contain navigation links (index.html, buy.html, code.html, studymanual.html, contact.html, returns.html, privacy.html, about.html),
       convert absolute hrefs that start with "/" into correct relative paths based on the file location.
    """
    run_step(instruction)
