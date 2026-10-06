# Python Learning Notes

My notes on Python and coding questions, kept as Jupyter notebooks. Each note puts
the problem write-up (Markdown), the solution (code), and its tests together in one file.

```
codingQuestions/
├── templates/
│   └── coding_question_template.ipynb   ← the blank note every new note starts from
├── notes/
│   └── 0001_two_sum.ipynb               ← a finished example to look at
├── new_note.py                          ← creates a new note from the template
├── pyproject.toml                       ← dependencies (managed by uv)
└── README.md                            ← this guide
```

## Quick start

```powershell
uv sync                                   # install dependencies (first time / new machine)
uv run new_note.py "Valid Parentheses"    # create notes/000N_valid_parentheses.ipynb
uv run jupyter lab                        # or just open the notebook in PyCharm
```

## Contents

1. [What is a Jupyter notebook?](#1-what-is-a-jupyter-notebook)
2. [Opening notebooks](#2-opening-notebooks)
3. [Keyboard shortcuts](#3-keyboard-shortcuts)
4. [Workflow for a new coding question](#4-workflow-for-a-new-coding-question)
5. [Markdown syntax cheat sheet](#5-markdown-syntax-cheat-sheet)
6. [Tips and common pitfalls](#6-tips-and-common-pitfalls)

---

## 1. What is a Jupyter notebook?

A notebook (`.ipynb`) is a list of **cells**. There are two kinds:

| Cell type    | What it holds                        | When you run it                    |
|--------------|--------------------------------------|------------------------------------|
| **Markdown** | Formatted text, tables, math, links  | It turns into formatted text       |
| **Code**     | Python                               | Python runs it and shows output below |

All code cells share one running Python process, called the **kernel**. Once you run a
cell that defines `def solve(...)`, every later cell can use `solve`. This is the
most important idea to understand about notebooks:

> ⚠️ **Order matters, and so does what you've already run.** The kernel remembers
> what you *ran*, not what's currently written on the page. If you edit a function,
> **re-run that cell** before running the tests again. If things get confusing,
> use **Restart Kernel and Run All**.

---

## 2. Opening notebooks

### Option A: in PyCharm (you're already using it)
1. Open any `.ipynb` file. PyCharm shows it as a notebook.
2. At the top, make sure the interpreter/kernel is this project's `.venv`.
3. Click ▶ next to a cell, or press **Shift+Enter**, to run it.

### Option B: JupyterLab in the browser
From the project folder:
```powershell
uv run jupyter lab
```
A browser tab opens. Use the file panel on the left to open notebooks.
Press **Ctrl+C** in the terminal to stop the server when you're finished.

---

## 3. Keyboard shortcuts

Jupyter has two modes:
- **Edit mode**: you're typing inside a cell (green/blue cursor).
- **Command mode**: the whole cell is selected. Press **Esc** to get here.

| Shortcut              | Mode    | Action                                   |
|-----------------------|---------|------------------------------------------|
| `Shift + Enter`       | any     | Run cell, move to the next one           |
| `Ctrl + Enter`        | any     | Run cell, stay on it                     |
| `Alt + Enter`         | any     | Run cell, insert a new cell below        |
| `Esc` / `Enter`       | —       | Switch to command mode / edit mode       |
| `A` / `B`             | command | Insert cell **A**bove / **B**elow        |
| `D` `D`               | command | Delete cell (press D twice)              |
| `M` / `Y`             | command | Change cell to **M**arkdown / code       |
| `Z`                   | command | Undo cell deletion                       |
| `Shift + ↑/↓`         | command | Select several cells                     |
| `0` `0`               | command | Restart kernel                           |
| `Tab`                 | edit    | Autocomplete                             |
| `Shift + Tab`         | edit    | Show a function's signature/docs (JupyterLab) |

These are JupyterLab's shortcuts. PyCharm's notebook editor uses most of them too.

---

## 4. Workflow for a new coding question

1. **Create a new note** from the template:
   ```powershell
   uv run new_note.py "Valid Parentheses"
   # or fill in more of the header at the same time:
   uv run new_note.py "Valid Parentheses" -d Easy -t "stack, string" -u https://leetcode.com/problems/valid-parentheses/
   ```
   This creates `notes/0002_valid_parentheses.ipynb`, numbered automatically, with the
   title and today's date already filled in. Run `uv run new_note.py -h` to see all options.
2. **Fill in the rest of the header table** and the problem statement.
3. **Write your thinking** before you write any code: brute force, key insight, edge cases.
4. **Run the Setup cell** (it loads `ipytest`).
5. **Write the solution** in the Solution cell and run it.
6. **Add test cases**, then run the Tests cell. Green dots = passing, `F` = failing.
7. Fix the code → **re-run the solution cell** → re-run the tests.
8. Fill in **Takeaways**. This is the part that helps most when you review later.

### How the tests work

The template uses [pytest](https://docs.pytest.org/) through
[ipytest](https://github.com/chmp/ipytest), so you can run pytest from inside a notebook:

```python
%%ipytest -q

CASES = [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 3], 6, [0, 1]),
]

@pytest.mark.parametrize("nums, target, expected", CASES)
def test_two_sum(nums, target, expected):
    assert two_sum(nums, target) == expected
```

- `%%ipytest` at the top of a cell runs every `test_*` function in that cell.
- `parametrize` runs the test once for each row in `CASES`. To add a case, add a row.
- You can test several implementations against the same cases. See `notes/0001_two_sum.ipynb`.
- For a quick check without pytest, a plain `assert solve(x) == y` in any cell also works.

### Useful "magic" commands

| Magic             | What it does                                       |
|-------------------|----------------------------------------------------|
| `%timeit expr`    | Times a single expression (good for comparing solutions) |
| `%%time`          | Times the whole cell (put it on the first line)    |
| `%%ipytest`       | Runs the pytest tests defined in the cell          |
| `%who`            | Lists the variables currently in memory            |
| `?obj`            | Shows the docs for `obj`, e.g. `?sorted`           |

---

## 5. Markdown syntax cheat sheet

Write these in **Markdown cells**, then run the cell to see the formatted result.
Double-click a rendered cell to edit it again.

### Headings
```markdown
# Heading 1   (one per notebook: the title)
## Heading 2  (sections)
### Heading 3 (sub-sections)
```

### Text styling
| You type                 | You get              |
|--------------------------|----------------------|
| `**bold**`               | **bold**             |
| `*italic*`               | *italic*             |
| `~~strikethrough~~`      | ~~strikethrough~~    |
| `` `inline code` ``      | `inline code`        |
| `[link](https://python.org)` | [link](https://python.org) |

Leave a **blank line** between paragraphs. A single line break is not enough.

### Lists
```markdown
- bullet item
- another item
  - nested item (indent 2 spaces)

1. numbered item
2. second item

- [ ] todo checkbox
- [x] done checkbox
```

### Code blocks
Use three backticks, plus a language name to get syntax highlighting:

````markdown
```python
def hello():
    print("hi")
```
````

### Blockquotes (good for problem statements)
```markdown
> Given an array of integers, return ...
```

### Tables
```markdown
| Approach    | Time    | Space |
|-------------|---------|-------|
| Brute force | O(n^2)  | O(1)  |
| Hash map    | O(n)    | O(n)  |
```
Add colons to the dash row to align columns: `|:---|` left, `|:---:|` center, `|---:|` right.

### Math (useful for complexity)
```markdown
Inline: $O(n \log n)$

Block:
$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$
```
Common symbols: `\log`, `n^2`, `x_i`, `\le`, `\ge`, `\ne`, `\cdot`, `\infty`.

### Horizontal line, images
```markdown
---
![alt text](path/or/url/to/image.png)
```

### Escaping
Put a backslash before a character to show it literally: `\*not italic\*`, `\#not a heading`.

---

## 6. Tips and common pitfalls

- **"NameError: name 'solve' is not defined"**: the cell that defines it hasn't been
  run yet. Run the cells from the top, or use *Run All*.
- **Tests still fail after a fix**: you edited the function but didn't re-run its cell.
- **Before you finish a note**, do *Restart Kernel → Run All* to make sure it works
  from top to bottom.
- **Long or infinite loop?** Use the ■ *Interrupt* button (or press `I` `I` in command mode).
- **Clearing outputs** (*Edit → Clear All Outputs*) before committing keeps git diffs small.
- **Installing a package**: run `uv add <package>` in the terminal, then restart the kernel.
