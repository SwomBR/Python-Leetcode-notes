
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import re
import sys

SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "WeCode-Community-Dev/FAANG-Coding-Interview-Questions/"
    "main/TopLeetCodeProblems.md"
)

SOURCE_PAGE = (
    "https://github.com/WeCode-Community-Dev/"
    "FAANG-Coding-Interview-Questions/blob/main/"
    "TopLeetCodeProblems.md"
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "LeetCode_Notes"

# Keep existing files safe.
OVERWRITE_EXISTING = False


def download_source():
    request = Request(
        SOURCE_URL,
        headers={"User-Agent": "LeetCode-Notes-Generator"}
    )

    try:
        with urlopen(request, timeout=30) as response:
            content = response.read().decode("utf-8")

        if not content.strip():
            raise ValueError("The source file is empty.")

        return content

    except (URLError, TimeoutError, ValueError) as error:
        raise RuntimeError(
            f"Could not download the source list: {error}"
        ) from error


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "_", value)
    return value.strip("_") or "untitled"


def parse_problems(markdown):
    problems = []
    current_topic = "General"
    by_title = {}

    for line in markdown.splitlines():
        heading = re.match(
            r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$",
            line
        )

        if heading:
            heading_text = heading.group(1).strip()

            if heading_text.lower() not in {
                "top leetcode problems",
                "table of contents",
                "contents",
            }:
                current_topic = heading_text

            continue

        item = re.match(
            r"^\s*[-*+]\s+(?:\[[ xX]\]\s*)?"
            r"\[([^\]]+)\]\((https?://[^)]+)\)",
            line
        )

        if not item:
            continue

        title = item.group(1).strip()
        url = item.group(2).strip()

        if not title or "leetcode.com/problems/" not in url:
            continue

        key = title.casefold()

        if key in by_title:
            existing = by_title[key]
            if current_topic not in existing["topics"]:
                existing["topics"].append(current_topic)
            continue

        problem = {
            "title": title,
            "topic": current_topic,
            "topics": [current_topic],
            "url": url,
            "status": "Not started",
            "note_file": ""
        }

        by_title[key] = problem
        problems.append(problem)

    if not problems:
        raise ValueError(
            "No linked LeetCode problems were detected. "
            "Check the source file's Markdown format."
        )

    return problems


def create_problem_markdown(problem, number):
    title = problem["title"]
    topic = problem["topic"]
    url = problem["url"]

    lines = [
        "# PYTHON NOTES",
        "",
        f"**Source list:** [{SOURCE_PAGE}]({SOURCE_PAGE})",
        "",
        f"## Problem — {topic}",
        "",
        f"**Problem {number}: {title}**",
        "",
        f"**LeetCode:** {url}",
        "",
        "**Difficulty:** To be verified",
        "",
        "**Progress:** Not started",
        "",
        "## 1. PROBLEM STATEMENT",
        "",
        f"Explain the requirements of {title} in your own words.",
        "Include all important rules and constraints.",
        "",
        "## 2. EXAMPLES",
        "",
        "### Example 1",
        "",
        "**Input:** Add the verified input here.",
        "",
        "**Output:** Add the verified output here.",
        "",
        "**Explanation:** Explain why the output is correct.",
        "",
        "### Additional examples",
        "",
        "Add the other verified examples and explanations.",
        "",
        "## 3. CONSTRAINTS",
        "",
        "Record the verified input limits and special rules.",
        "",
        "## 4. LOGIC — EXPLAIN LIKE A BEGINNER",
        "",
        "Use an everyday story to explain the problem.",
        "Explain what we know, what we need, and why the logic works.",
        "",
        "### Step-by-step algorithm",
        "",
        "1. First step.",
        "2. Next step.",
        "3. Explain how the answer is obtained.",
        "",
        "## 5. BRUTE-FORCE SOLUTION",
        "",
        "Explain the simplest correct approach and its limitations.",
        "",
        "```python",
        "# Add the complete brute-force solution.",
        "```",
        "",
        "**Time complexity:** To be verified.",
        "",
        "**Auxiliary space:** To be verified.",
        "",
        "## 6. OPTIMIZED SOLUTION",
        "",
        "Explain the improvement and why it works.",
        "",
        "### Python code",
        "",
        "```python",
        "# Add the complete, verified LeetCode solution.",
        "```",
        "",
        "### Line-by-line explanation",
        "",
        "Explain variables, loops, conditions, data structures,",
        "and return values in beginner-friendly language.",
        "",
        "## 7. DRY RUN",
        "",
        "| Step | Current value | Memory / variables | Action |",
        "|---|---|---|---|",
        "| 1 | — | — | Initialize the algorithm |",
        "| 2 | — | — | Process the input |",
        "| 3 | — | — | Continue until the result is found |",
        "",
        "Replace this table with a real walkthrough.",
        "",
        "## 8. CONCEPTS",
        "",
        "Explain each data structure, algorithm, and Python concept.",
        "Link to relevant foundation lessons in this repository.",
        "",
        "## 9. COMPLEXITY ANALYSIS",
        "",
        "**Time:** Explain and verify the Big-O complexity.",
        "",
        "**Auxiliary space:** Explain additional memory usage.",
        "",
        "## 10. EDGE CASES",
        "",
        "List problem-specific boundary cases and expected results.",
        "",
        "## 11. COMMON MISTAKES",
        "",
        "Explain likely bugs and how to avoid them.",
        "",
        "## 12. PRACTICE QUESTIONS",
        "",
        "Add exercises, hints, and worked answers.",
        "",
        "## 13. REVISION CARD",
        "",
        "- **Pattern:** To be identified.",
        "- **Key idea:** To be completed.",
        "- **Time complexity:** To be verified.",
        "- **Auxiliary space:** To be verified.",
        "",
        "## 14. COMPLETION CHECKLIST",
        "",
        "- [ ] Problem requirements verified",
        "- [ ] Examples and constraints verified",
        "- [ ] Beginner-friendly logic completed",
        "- [ ] Brute-force solution reviewed",
        "- [ ] Optimized Python solution reviewed",
        "- [ ] Dry run completed",
        "- [ ] Complexity verified",
        "- [ ] Edge cases tested",
        "- [ ] Practice questions added",
        "- [ ] Final review completed",
        "",
    ]

    return "\n".join(lines)


def main():
    print("Downloading the original problem list...")
    source = download_source()
    problems = parse_problems(source)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    (OUTPUT_DIR / "source_problem_list.md").write_text(
        source, encoding="utf-8"
    )

    topic_folders = {}
    created = 0
    skipped = 0
    index_lines = [
        "# Python LeetCode Study Notes",
        "",
        f"**Unique problems detected:** {len(problems)}",
        "",
        "Each problem has its own detailed study-note file.",
        "Files still need their explanations and solutions completed.",
        "",
        "## Problems by topic",
        "",
    ]

    for number, problem in enumerate(problems, start=1):
        topic = problem["topic"]

        if topic not in topic_folders:
            folder_name = (
                f"{len(topic_folders) + 1:02d}_"
                f"{slugify(topic)}"
            )
            topic_folders[topic] = folder_name

        filename = (
            f"{number:03d}_{slugify(problem['title'])}.md"
        )

        folder = OUTPUT_DIR / topic_folders[topic]
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / filename
        relative_path = file_path.relative_to(
            OUTPUT_DIR
        ).as_posix()

        problem["note_file"] = relative_path

        if file_path.exists() and not OVERWRITE_EXISTING:
            skipped += 1
        else:
            file_path.write_text(
                create_problem_markdown(problem, number),
                encoding="utf-8"
            )
            created += 1

        index_lines.append(
            f"- [ ] [{problem['title']}]({relative_path})"
            f" — {topic}"
        )

    index_lines.extend([
        "",
        "## Source",
        "",
        f"[Original problem collection]({SOURCE_PAGE})",
        "",
    ])

    (OUTPUT_DIR / "README.md").write_text(
        "\n".join(index_lines), encoding="utf-8"
    )

    (OUTPUT_DIR / "problems_manifest.json").write_text(
        json.dumps(problems, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    tracker = [
        "# LeetCode Progress Tracker",
        "",
        f"- Unique problems detected: {len(problems)}",
        "- Completed solutions: 0 verified by this generator",
        f"- Notes created or updated: {created}",
        f"- Existing notes skipped: {skipped}",
        "",
        "A generated template is not a completed solution.",
        "Update completion status only after reviewing the content.",
        "",
    ]

    (OUTPUT_DIR / "PROGRESS_TRACKER.md").write_text(
        "\n".join(tracker), encoding="utf-8"
    )

    print("\nGeneration finished.")
    print(f"Unique problems: {len(problems)}")
    print(f"Created/updated files: {created}")
    print(f"Existing files skipped: {skipped}")
    print(f"Topic folders: {len(topic_folders)}")
    print(f"Output: {OUTPUT_DIR}")
    print("\nReview LeetCode_Notes/README.md next.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        sys.exit(1)