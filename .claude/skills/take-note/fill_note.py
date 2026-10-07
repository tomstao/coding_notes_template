"""Fill a note created by new_note.py with cells from a JSON spec.

Usage:
    uv run .claude/skills/take-note/fill_note.py notes/0217_contains_duplicate.ipynb spec.json

spec.json:
    {
      "status": "Solved",                       # replaces "Solved / Needs review / Stuck"
      "cells": [
        {"markdown": "## 1. Problem\n..."},
        {"setup": true},                        # the template's ipytest setup cell, kept as is
        {"code": "def solve(...): ..."},
        ...
      ]
    }

The header cell (title/source/difficulty/topics/date table) is always kept as the first cell.
"""
import json
import sys
import uuid
from pathlib import Path


def cell(kind: str, text: str) -> dict:
    c = {"cell_type": kind, "id": uuid.uuid4().hex[:12], "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}
    if kind == "code":
        c.update(execution_count=None, outputs=[])
    return c


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    note, spec = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    nb = json.loads(note.read_text(encoding="utf-8"))

    header = nb["cells"][0]
    setup = next(c for c in nb["cells"] if c["cell_type"] == "code" and "ipytest.autoconfig()" in "".join(c["source"]))
    if status := spec.get("status"):
        placeholder = "Solved / Needs review / Stuck"
        text = "".join(header["source"]).replace(placeholder, status.ljust(len(placeholder)))
        header["source"] = text.splitlines(keepends=True)

    cells = [header]
    for item in spec["cells"]:
        if item.get("setup"):
            cells.append(setup)
        elif "markdown" in item:
            cells.append(cell("markdown", item["markdown"]))
        elif "code" in item:
            cells.append(cell("code", item["code"]))
        else:
            sys.exit(f"unknown cell spec: {item}")

    nb["cells"] = cells
    note.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Filled {note} with {len(cells)} cells")


if __name__ == "__main__":
    main()
