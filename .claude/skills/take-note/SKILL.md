---
name: take-note
description: Record a coding question (LeetCode or similar) as a Jupyter note in notes/ using the repo template — the user's own solution, why it's slow, the best-practice solution(s), tests, timing, and the pattern to remember. Use when the user pastes a problem and/or their solution and asks to take a note, record it, or asks "what's the best practice / the pattern" for it.
---

# Take a note for a coding question

The user pastes a problem statement and usually their own solution. Turn it into a
complete, verified note in `notes/`, built from `templates/coding_question_template.ipynb`,
and explain the result in chat.

## 1. Create the note from the template

```bash
uv run new_note.py "<Title>" -d <Easy|Medium|Hard> -t "<topic1>,<topic2>" -u <problem URL> -n <number>
```

- `-n`: use the **LeetCode problem number** when there is one (Two Sum → `0001`,
  Contains Duplicate → `0217`). Otherwise omit it and the next free number is used.
- `-u`: the canonical problem URL, e.g. `https://leetcode.com/problems/<slug>/`.
- `-t`: the topics that matter for the solution (e.g. `array,hash set,sorting`).
- Never overwrite an existing note; if the file already exists, ask the user.

## 2. Work out the content

Before writing, decide:
- **The user's solution:** is it correct? What is its time/space complexity, and *exactly
  which operations* make it slow (e.g. `list.pop(0)` is O(n), `x in list` is O(n),
  sorting is O(n log n), it mutates its input). If there is no user solution, skip Approach A.
- **Better approaches:** usually 1–3, ending with the one to remember. Mark the best
  one with `✅ best practice`. If the most Pythonic version differs from the
  interview-standard one, include both and say which is which.
- **The pattern:** the general rule this problem teaches ("have I seen this before?" →
  hash set; "same elements, any order" → compare counts; …).

## 3. Fill every section

Write a JSON spec (in a temp/scratch location, not in the repo) and apply it:

```bash
uv run .claude/skills/take-note/fill_note.py notes/<file>.ipynb <spec.json>
```

Spec cells, in this order (see `fill_note.py` for the format; the header cell is kept automatically,
set `"status": "Solved"` unless the user says otherwise):

1. `## 1. Problem` — the statement as a `>` quote, every example in a fenced block
   (`Input:` / `Output:`), and the constraints as a bullet list.
2. `## 2. Thinking` — **Brute force idea**, **Key insight**, **Edge cases to remember**
   (plus a quick-reject check if there is one). Use `$O(\cdot)$` math.
3. `{"setup": true}` — the template's ipytest setup cell.
4. `## 3. Solution` then, per approach, a markdown cell
   `### Approach X — <name>` with **Complexity:** Time $O(?)$ · Space $O(?)$ and 1–3
   sentences, followed by a code cell. Approach A is the user's code, **unchanged**
   except: a plain snake_case function instead of the `class Solution` method,
   `list[int]` instead of `List[int]`, and short comments pointing at the slow lines.
   All approaches share one signature and use descriptive names
   (`has_duplicate_mine`, `has_duplicate_sort`, `has_duplicate`, …).
5. `## 4. Tests` — one `%%ipytest -q` cell with a `CASES` list (all the problem's
   examples + edge cases with a `# comment` saying what each covers) and a test
   parametrized over **every approach** and every case. If any approach mutates its
   input, pass a copy (`list(nums)`) and say why.
6. `## 5. Scratch / Experiments` — a `%timeit` comparison on a worst-case input near the
   max constraint size (shrink it and say so if the slow approach would take too long).
   If Big-O and the measured times disagree (e.g. a C-implemented builtin beats a Python
   loop), explain why.
7. `## 6. Takeaways` — **Pattern**, **Mistakes I made** (what was suboptimal in the user's
   solution, phrased as lessons), **Related problems** (with LeetCode numbers, and how
   each relates).

Match the style of the existing notes in `notes/` (look at one if unsure).

## 4. Verify

Execute the whole notebook and check that every test passes and timings print:

```bash
uv run jupyter nbconvert --to notebook --execute --stdout notes/<file>.ipynb > /dev/null
```

Then read the outputs (pipe `--stdout` into a small script that prints each cell's
`outputs[].text`). Fix and re-run until it's clean. Do **not** save executed outputs
into the note — keep it output-free like the template.

## 5. Report back in chat

Answer the user's actual questions concisely:
- **Why theirs is slow / not ideal** — point at the specific lines.
- **Best practice** — the code, as a `class Solution` method so it's paste-ready for LeetCode,
  with its complexity.
- **The pattern** — one or two sentences.
- **What's in the note** — approaches, number of passing tests, the timing table.

## 6. Git

Do not commit unless asked. When the user says "commit and push":
`git add notes/<file>.ipynb`, commit with the message `Add <Title> note (#<number>)`,
push, and confirm the branch is in sync with its remote.
