"""Create a new note in notes/ from the template.

Usage:
    uv run new_note.py "Valid Parentheses"
    uv run new_note.py "Valid Parentheses" -d Easy -t stack,string -u https://leetcode.com/problems/valid-parentheses/
"""
import argparse
import json
import re
import uuid
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "templates" / "coding_question_template.ipynb"
NOTES = ROOT / "notes"


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")


def next_number() -> int:
    numbers = [int(m.group(1)) for p in NOTES.glob("*.ipynb") if (m := re.match(r"(\d+)_", p.name))]
    return max(numbers, default=0) + 1


def main():
    parser = argparse.ArgumentParser(description="Create a new note from the template.")
    parser.add_argument("title", help='problem title, e.g. "Two Sum"')
    parser.add_argument("-d", "--difficulty", help="Easy / Medium / Hard")
    parser.add_argument("-t", "--topics", help="comma-separated, e.g. array,hash map")
    parser.add_argument("-u", "--url", help="link to the problem")
    parser.add_argument("-n", "--number", type=int, help="note number (default: next free number)")
    args = parser.parse_args()

    number = args.number or next_number()
    path = NOTES / f"{number:04d}_{slugify(args.title)}.ipynb"
    if path.exists():
        parser.error(f"{path.relative_to(ROOT)} already exists")

    replacements = {
        "<Problem Title>": args.title,
        "YYYY-MM-DD": date.today().isoformat(),
    }
    if args.difficulty:
        replacements["Easy / Medium / Hard"] = args.difficulty.capitalize()
    if args.topics:
        replacements["`array`, `hash map`"] = ", ".join(f"`{t.strip()}`" for t in args.topics.split(","))
    if args.url:
        replacements["[LeetCode #000](https://leetcode.com/)"] = f"[link]({args.url})"

    nb = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        cell["id"] = uuid.uuid4().hex[:12]
        if cell["cell_type"] == "markdown":
            text = "".join(cell["source"])
            for old, new in replacements.items():
                text = text.replace(old, new)
            cell["source"] = text.splitlines(keepends=True)

    NOTES.mkdir(exist_ok=True)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
