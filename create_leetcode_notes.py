
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
import re
import json
import sys


# ============================================================
# CONFIGURATION
# ============================================================

SOURCE_URL = (
    "https://raw.githubusercontent.com/"
    "WeCode-Community-Dev/FAANG-Coding-Interview-Questions/"
    "main/TopLeetCodeProblems.md"
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "LeetCode_Notes"

# False = never overwrite existing notes.
OVERWRITE_EXISTING = False


# ============================================================
# DOWNLOAD THE SOURCE FILE
# ============================================================

def download_source():
    request = Request(
        SOURCE_URL,
        headers={"User-Agent": "LeetCode-Notes-Generator"}
    )

    try:
        with urlopen(request, timeout=30) as response:
            content = response.read().decode("utf-8")

        if not content.strip():
            raise ValueError("The downloaded source file is empty.")

        if "404: Not Found" in content[:200]:
            raise ValueError("GitHub returned a 404 error.")

        print("Source downloaded successfully.")
        return content

    except (URLError, TimeoutError, ValueError) as error:
        raise RuntimeError(
            f"Could not download the problem list: {error}\n"
            "Check your internet connection and the GitHub URL."
        ) from error


# ============================================================
# PARSE THE MARKDOWN SOURCE
# ============================================================

def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value)
    return value.strip("-") or "untitled"


def parse_problems(markdown):
    problems = []
    current_topic = "General"
    seen = set()

    for line in markdown.splitlines():
        heading = re.match(
            r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$",
            line
        )

        if heading:
            heading_text = heading.group(1).strip()

            # Ignore the document's main title.
            if not problems or len(heading_text) < 100:
                current_topic = heading_text

            continue

        # Only inspect Markdown list entries.
        item = re.match(r"^\s*[-*+]\s+(.+?)\s*$", line)

        if not item:
            continue

        entry = item.group(1).strip()
        title = None
        problem_url = None

        # Format: [Two Sum](https://leetcode.com/problems/two-sum/)
        link_match = re.match(
            r"^\[([^\]]+)\]\((https?://[^)]+)\)",
            entry
        )

        if link_match:
            title = link_match.group(1).strip()
            problem_url = link_match.group(2).strip()

        # Format: [Input] Two Sum
        elif re.match(r"^\[Input\]\s+", entry, re.IGNORECASE):
            title = re.sub(
                r"^\[Input\]\s+",
                "",
                entry,
                flags=re.IGNORECASE
            ).strip()

        else:
            # Support simple bullet lists of problem names.
            # Ignore ordinary prose and long descriptions.
            plain = re.sub(r"`", "", entry).strip()

            if (
                len(plain) <= 100
                and not plain.startswith("[")
                and not plain.startswith("http")
                and not plain.endswith(":")
            ):
                title = plain

        if not title:
            continue

        # Ignore obvious navigation and non-problem headings.
        if title.lower() in {
            "input", "output", "table of contents",
            "readme", "leetcode", "problems"
        }:
            continue

        # Ignore duplicates while preserving source order.
        key = (current_topic.lower(), title.lower())

        if key in seen:
            continue

        seen.add(key)

        problems.append({
            "title": title,
            "topic": current_topic,
            "url": problem_url or (
                "https://leetcode.com/problems/"
                + slugify(title) + "/"
            )
        })

    if not problems:
        raise ValueError(
            "No problems were detected in the source.\n"
            "The source Markdown format may need a parser adjustment."
        )

    return problems


# ============================================================
# CREATE THE STUDY TEMPLATE
# ============================================================

def create_problem_markdown(problem, number):
    title = problem["title"]
    topic = problem["topic"]
    url = problem["url"]

    # Build the document as a list of lines. This avoids
    # nested multiline-string syntax errors.
    lines = [
        f"# {number:03d}. {title}",
        "",
        f"- **Topic:** {topic}",
        "- **Difficulty:** To be verified",
        f"- **LeetCode:** [{title}]({url})",
        "- **Progress:** Not started",
        "",
        "## 1. Problem in Simple English",
        "",
        "Explain the problem in beginner-friendly language.",
        "",
        "## 2. Problem Statement",
        "",
        "Summarize the requirements and constraints.",
        "",
        "## 3. Examples",
        "",
        "### Example 1",
        "",
        "**Input:**",
        "",
        "Add the example input here.",
        "",
        "**Output:**",
        "",
        "Add the expected output here.",
        "",
        "**Explanation:**",
        "",
        "Explain why the output is correct.",
        "",
        "## 4. What Is This Problem Testing?",
        "",
        "- Data structures:",
        "- Algorithms:",
        "- Important constraints:",
        "",
        "## 5. Brute-Force Approach",
        "",
        "Explain the simplest correct approach.",
        "",
        "### Logic",
        "",
        "1. Describe the first step.",
        "2. Describe the next step.",
        "3. Explain how the answer is obtained.",
        "",
        "### Complexity",
        "",
        "- **Time:** To be determined",
        "- **Space:** To be determined",
        "",
        "## 6. Optimized Approach",
        "",
        "Explain the intuition behind the improved solution.",
        "",
        "### Algorithm",
        "",
        "1. Step one.",
        "2. Step two.",
        "3. Step three.",
        "",
        "## 7. Python Solution",
        "",
        "```python",
        "# Add the complete, verified solution here.",
        "```",
        "",
        "### Explain the Code",
        "",
        "Explain important lines, variables, conditions, and loops.",
        "",
        "## 8. Dry Run",
        "",
        "| Step | Current value | Variables | What happens? |",
        "|---|---|---|---|",
        "| 1 | — | — | Start the algorithm |",
        "| 2 | — | — | Process the input |",
        "| 3 | — | — | Obtain the result |",
        "",
        "## 9. Complexity Analysis",
        "",
        "- **Time complexity:** To be determined and explained.",
        "- **Space complexity:** To be determined and explained.",
        "",
        "## 10. Edge Cases",
        "",
        "- Empty or minimum-size input, if permitted.",
        "- Duplicate values, if relevant.",
        "- Negative numbers or zero, if relevant.",
        "- Maximum constraints and boundary cases.",
        "",
        "## 11. Common Mistakes",
        "",
        "Explain mistakes specific to this problem.",
        "",
        "## 12. Key Takeaway",
        "",
        "Explain the reusable problem-solving pattern.",
        "",
        "## 13. Practice Variations",
        "",
        "1. Variation one.",
        "2. Variation two.",
        "",
        "## 14. Revision Checklist",
        "",
        "- [ ] I understand the problem.",
        "- [ ] I can explain the logic without notes.",
        "- [ ] I can write the solution independently.",
        "- [ ] I understand time and space complexity.",
        "- [ ] I tested the important edge cases.",
        ""
    ]

    return "\n".join(lines)


# ============================================================
# GENERATE ALL FILES
# ============================================================

def main():
    print("=" * 55)
    print("       LEETCODE MARKDOWN NOTES GENERATOR")
    print("=" * 55)

    source = download_source()
    problems = parse_problems(source)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save the original list for reference.
    (OUTPUT_DIR / "source_problem_list.md").write_text(
        source,
        encoding="utf-8"
    )

    # Keep track of topic folders and problem numbers.
    topic_folders = {}
    topic_counts = {}
    index_lines = [
        "# Python LeetCode Interview Notes",
        "",
        f"**Problems detected:** {len(problems)}",
        "",
        "Open an individual problem to study its logic and solution.",
        "",
        "## Table of Contents",
        ""
    ]

    created = 0
    skipped = 0

    for number, problem in enumerate(problems, start=1):
        topic = problem["topic"]

        if topic not in topic_folders:
            folder_name = (
                f"{len(topic_folders) + 1:02d}_"
                f"{slugify(topic)}"
            )

            topic_folders[topic] = folder_name
            topic_counts[topic] = 0

        topic_counts[topic] += 1

        folder = OUTPUT_DIR / topic_folders[topic]
        folder.mkdir(parents=True, exist_ok=True)

        filename = (
            f"{number:03d}_"
            f"{slugify(problem['title'])}.md"
        )

        file_path = folder / filename
        relative_path = file_path.relative_to(
            OUTPUT_DIR
        ).as_posix()

        if file_path.exists() and not OVERWRITE_EXISTING:
            skipped += 1
        else:
            content = create_problem_markdown(problem, number)

            file_path.write_text(
                content,
                encoding="utf-8"
            )

            created += 1

        index_lines.append(
            f"- [ ] [{problem['title']}]({relative_path}) "
            f"— {topic}"
        )

    # Create the master index.
    index_lines.extend([
        "",
        "## Generation Summary",
        "",
        f"- Problems detected: {len(problems)}",
        f"- Files created or replaced: {created}",
        f"- Existing files skipped: {skipped}",
        "",
        "## Source",
        "",
        f"[Original GitHub list]({SOURCE_URL})",
        ""
    ])

    (OUTPUT_DIR / "README.md").write_text(
        "\n".join(index_lines),
        encoding="utf-8"
    )

    # Save a manifest for future automation.
    (OUTPUT_DIR / "problems_manifest.json").write_text(
        json.dumps(problems, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print()
    print("SUCCESS!")
    print(f"Output folder: {OUTPUT_DIR}")
    print(f"Problems detected: {len(problems)}")
    print(f"Files created or replaced: {created}")
    print(f"Existing files skipped: {skipped}")
    print(f"Topic folders: {len(topic_folders)}")
    print()
    print("Open LeetCode_Notes/README.md to browse your notes.")
    print("Note: generated files contain study templates, not solutions.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        sys.exit(1)