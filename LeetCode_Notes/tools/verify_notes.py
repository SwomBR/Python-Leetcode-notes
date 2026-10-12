"""Verify LeetCode study notes and rebuild the progress tracker.

What it checks for every problem in problems_manifest.json:
  * the note contains all 14 required section headings;
  * no leftover template placeholder text remains;
  * every ```python block in the note runs without errors;
  * every block that defines the tested class (usually `Solution`) passes
    the test cases in tools/tests/pNNN.py.

Statuses are stored in problems_manifest.json and are set by a reviewer:
  Pending   - note not written yet
  Completed - note written, awaiting review
  Reviewed  - note written, automated checks pass, content reviewed
  Blocked   - cannot be completed (reason in "blocker")

A note is never reported as Reviewed by this script unless its checks pass.

Usage (from the LeetCode_Notes folder or anywhere):
    python tools/verify_notes.py            # check notes, rebuild tracker
    python tools/verify_notes.py 001 002    # check only these problems
    python tools/verify_notes.py --check-only 006   # check, do not rewrite tracker/README
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "problems_manifest.json"
TRACKER = ROOT / "PROGRESS_TRACKER.md"
README = ROOT / "README.md"
TESTS_DIR = Path(__file__).resolve().parent / "tests"

REQUIRED_SECTIONS = [
    "## 1. Problem Overview",
    "## 2. Problem Explanation",
    "## 3. Everyday Analogy",
    "## 4. Step-by-Step Logic",
    "## 5. Brute-Force Solution",
    "## 6. Optimized Solution",
    "## 7. Line-by-Line Explanation",
    "## 8. Dry Run",
    "## 9. Concepts",
    "## 10. Complexity Analysis",
    "## 11. Edge Cases",
    "## 12. Common Mistakes",
    "## 13. Practice Questions",
    "## 14. Revision Summary",
]

PLACEHOLDERS = [
    "Add the verified",
    "Add the complete",
    "To be verified",
    "To be determined",
    "To be identified",
    "To be completed",
    "Replace this table",
    "Explain the requirements of",
]

PRELUDE = '''
from typing import *
import collections, heapq, math, bisect, itertools, functools, string
from collections import Counter, defaultdict, deque, OrderedDict
from functools import lru_cache, cache

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
'''

CODE_BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)


def load_test_module(number: str):
    path = TESTS_DIR / f"p{number}.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"p{number}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_note(entry: dict) -> tuple[list[str], int]:
    """Return (problems found, solution blocks tested); no problems = pass."""
    errors: list[str] = []
    note_path = ROOT / entry["note_file"]
    number = Path(entry["note_file"]).name[:3]
    text = note_path.read_text(encoding="utf-8")

    for heading in REQUIRED_SECTIONS:
        if heading not in text:
            errors.append(f"missing section '{heading}'")
    for phrase in PLACEHOLDERS:
        if phrase in text:
            errors.append(f"template placeholder still present: '{phrase}'")

    tests = load_test_module(number)
    if tests is None:
        errors.append(f"no test file tools/tests/p{number}.py")
        return errors, 0

    target = getattr(tests, "TARGET", "Solution")
    min_tested = getattr(tests, "MIN_TESTED_BLOCKS", 2)
    tested = 0
    for index, block in enumerate(CODE_BLOCK.findall(text), start=1):
        namespace: dict = {}
        try:
            exec(PRELUDE, namespace)
            exec(block, namespace)
        except Exception:
            errors.append(f"python block {index} failed to run:\n"
                          + traceback.format_exc(limit=2))
            continue
        if re.search(rf"^class {target}\b", block, re.MULTILINE):
            try:
                tests.check(namespace)
                tested += 1
            except Exception:
                errors.append(f"python block {index} failed tests:\n"
                              + traceback.format_exc(limit=3))
    if tested < min_tested:
        errors.append(f"only {tested} solution block(s) tested; "
                      f"expected at least {min_tested}")
    return errors, tested


def build_tracker(manifest: list[dict], results: dict[str, list[str]]) -> None:
    counts = {"Reviewed": 0, "Completed": 0, "Pending": 0, "Blocked": 0}
    rows = []
    for entry in manifest:
        number = Path(entry["note_file"]).name[:3]
        status = entry.get("status", "Pending")
        if status not in counts:
            status = "Pending"
        errors = results.get(number)
        if errors is None:
            check = "not run"
        elif errors:
            check = f"FAIL ({len(errors)})"
            if status == "Reviewed":
                status = "Completed"  # never claim Reviewed for a failing note
        else:
            check = "pass"
        counts[status] += 1
        note = entry.get("blocker") or entry.get("review_note", "")
        rows.append(
            f"| {number} | [{entry['title']}]({entry['note_file']}) "
            f"| {', '.join(entry['topics'])} | {status} | {check} | {note} |"
        )

    lines = [
        "# LeetCode Progress Tracker",
        "",
        f"- Unique problems: {len(manifest)}",
        f"- Reviewed: {counts['Reviewed']}",
        f"- Completed (awaiting review): {counts['Completed']}",
        f"- Pending: {counts['Pending']}",
        f"- Blocked: {counts['Blocked']}",
        "",
        "**Status meanings:** *Pending* = note not written; *Completed* = "
        "note written, awaiting review; *Reviewed* = all 14 sections written, "
        "every Python block runs and passes the tests in "
        "`tools/tests/`, and the content was reviewed; *Blocked* = cannot be "
        "completed (see notes column).",
        "",
        "Regenerate this file with `python tools/verify_notes.py`.",
        "",
        "| # | Problem | Topics | Status | Automated check | Notes |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
    ]
    TRACKER.write_text("\n".join(lines), encoding="utf-8")


def update_readme(manifest: list[dict]) -> None:
    text = README.read_text(encoding="utf-8")
    for entry in manifest:
        link = f"[{entry['title']}]({entry['note_file']})"
        mark = "x" if entry.get("status") == "Reviewed" else " "
        text = re.sub(r"- \[[ x]\] " + re.escape(link), f"- [{mark}] {link}", text)
    README.write_text(text, encoding="utf-8")


def main(argv: list[str]) -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check_only = "--check-only" in argv
    wanted = {arg for arg in argv if arg != "--check-only"}
    results: dict[str, list[str]] = {}
    failures = 0
    for entry in manifest:
        number = Path(entry["note_file"]).name[:3]
        if wanted and number not in wanted:
            continue
        if entry.get("status", "Pending") == "Pending" and not wanted:
            continue
        errors, tested = check_note(entry)
        results[number] = errors
        label = "PASS" if not errors else "FAIL"
        print(f"[{label}] {number} {entry['title']} "
              f"({tested} solution blocks tested)")
        for error in errors:
            failures += 1
            print("    - " + error.replace("\n", "\n      "))
    if not check_only:
        build_tracker(manifest, results)
        update_readme(manifest)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
