"""Check that the plain-language principle files agree with themselves,
and that the files that link into them still point at existing headings.

Usage: python scripts/validate.py
Exit code 0 when every check passes, 1 when any check reports a problem.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIRECTORY = REPOSITORY_ROOT / "plain-language"
PRINCIPLE_FILES = [
    SKILL_DIRECTORY / "SKILL.md",
    SKILL_DIRECTORY / "references" / "english.md",
    SKILL_DIRECTORY / "references" / "japanese.md",
]
RETIRED_TABLE_FILE = SKILL_DIRECTORY / "SKILL.md"
# files outside the skill whose links into the principle files are checked
FILES_LINKING_TO_PRINCIPLES = [
    REPOSITORY_ROOT / "README.md",
    REPOSITORY_ROOT / "evals" / "README.md",
]

# matches "P302" and "J601"; does not match "P02" or "P802"
PRINCIPLE_ID = re.compile(r"^[PJE][1-7]\d\d$")
# matches "| [P302](#p302-order-information-by-purpose) | Lead with ... |"
INDEX_ROW = re.compile(r"^\| \[(?P<id>[PJE]\d{3})\]\((?P<anchor>#[^)]+)\) \| .+ \|$")
# matches "### P302 Order information by purpose"
PRINCIPLE_HEADING = re.compile(r"^### (?P<id>[PJE]\d{3}) (?P<title>.+)$")
# matches "## 3xx Discourse"; the digit is the level
LEVEL_HEADING = re.compile(r"^## (?P<level>[1-7])xx (?P<name>\w+)$")
# matches "# plain-language", "## Principle index", and "### P302 Order ..."
ANY_HEADING = re.compile(r"^#{1,3} (?P<text>.+)$")
# matches "](#p701-preserve-meaning)" and "](../SKILL.md#p101-adapt-to-the-reader-and-task)"
LINK_WITH_ANCHOR = re.compile(r"\]\((?P<target>[^)#]*)#(?P<anchor>[^)]+)\)")
# matches "| Retired ID | Successor | Note |" (the header of the retired table)
RETIRED_TABLE_HEADER = re.compile(r"^\| Retired ID \| Successor \| Note \|$")
# matches "| J603 | — | Long vowels are handled by J502. |" and "| P104 | P702 | Merged. |"
RETIRED_ROW = re.compile(r"^\| (?P<id>[PJE]\d{3}) \| (?P<successor>[^|]+?) \| .+ \|$")
# matches "```python" and "```" (fences that open or close a code block)
CODE_FENCE = re.compile(r"^```")

BACK_TO_INDEX_LINKS = {
    "[Back to the principle index](#principle-index)",
    "[索引に戻る](#索引)",
}
NO_SUCCESSOR = "—"


@dataclass
class Principle:
    id: str
    title: str
    level_of_section: str
    last_line: str


@dataclass
class PrincipleFile:
    path: Path
    lines: list[str]
    anchors: set[str]
    index_ids: dict[str, str]
    principles: list[Principle]


def display_path(path: Path) -> str:
    return path.relative_to(REPOSITORY_ROOT).as_posix()


def github_anchor(heading_text: str) -> str:
    lowered = heading_text.strip().lower()
    without_punctuation = re.sub(r"[^\w\s-]", "", lowered)
    return re.sub(r"\s+", "-", without_punctuation)


def strip_code_blocks(lines: list[str]) -> list[str]:
    kept: list[str] = []
    inside_code_block = False
    for line in lines:
        if CODE_FENCE.match(line):
            inside_code_block = not inside_code_block
            continue
        if inside_code_block:
            continue
        kept.append(line)
    return kept


def collect_anchors(lines: list[str]) -> set[str]:
    anchors: set[str] = set()
    for line in lines:
        heading = ANY_HEADING.match(line)
        if heading is None:
            continue
        anchors.add(github_anchor(heading.group("text")))
    return anchors


def collect_index_ids(lines: list[str]) -> dict[str, str]:
    anchor_by_id: dict[str, str] = {}
    for line in lines:
        row = INDEX_ROW.match(line)
        if row is None:
            continue
        anchor_by_id[row.group("id")] = row.group("anchor").lstrip("#")
    return anchor_by_id


def collect_principles(lines: list[str]) -> list[Principle]:
    principles: list[Principle] = []
    current_level = ""
    inside_principle = False
    for line in lines:
        level_heading = LEVEL_HEADING.match(line)
        if level_heading is not None:
            current_level = level_heading.group("level")
            inside_principle = False
            continue
        if line.startswith("## "):
            current_level = ""
            inside_principle = False
            continue
        principle_heading = PRINCIPLE_HEADING.match(line)
        if principle_heading is not None:
            principles.append(Principle(
                id=principle_heading.group("id"),
                title=principle_heading.group("title"),
                level_of_section=current_level,
                last_line="",
            ))
            inside_principle = True
            continue
        if inside_principle and line.strip():
            principles[-1].last_line = line.strip()
    return principles


def load_principle_file(path: Path) -> PrincipleFile:
    lines = strip_code_blocks(path.read_text(encoding="utf-8").splitlines())
    return PrincipleFile(
        path=path,
        lines=lines,
        anchors=collect_anchors(lines),
        index_ids=collect_index_ids(lines),
        principles=collect_principles(lines),
    )


def collect_retired_rows(lines: list[str]) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    inside_table = False
    for line in lines:
        if RETIRED_TABLE_HEADER.match(line):
            inside_table = True
            continue
        if not inside_table:
            continue
        if not line.startswith("|"):
            break
        row = RETIRED_ROW.match(line)
        if row is None:
            continue
        rows.append((row.group("id"), row.group("successor").strip()))
    return rows


def check_id_format(files: list[PrincipleFile]) -> list[str]:
    problems: list[str] = []
    for file in files:
        for principle in file.principles:
            if PRINCIPLE_ID.match(principle.id):
                continue
            problems.append(f"{display_path(file.path)}: {principle.id} is not a valid ID")
    return problems


def check_ids_unique(files: list[PrincipleFile]) -> list[str]:
    problems: list[str] = []
    file_by_id: dict[str, str] = {}
    for file in files:
        for principle in file.principles:
            earlier_file = file_by_id.get(principle.id)
            if earlier_file is not None:
                problems.append(f"{display_path(file.path)}: {principle.id} also appears in {earlier_file}")
                continue
            file_by_id[principle.id] = display_path(file.path)
    return problems


def check_index_matches_sections(file: PrincipleFile) -> list[str]:
    problems: list[str] = []
    section_ids = {principle.id for principle in file.principles}
    for principle_id in sorted(set(file.index_ids) - section_ids):
        problems.append(f"{display_path(file.path)}: {principle_id} is in the index but has no section")
    for principle_id in sorted(section_ids - set(file.index_ids)):
        problems.append(f"{display_path(file.path)}: {principle_id} has a section but is not in the index")
    for principle in file.principles:
        expected_anchor = github_anchor(f"{principle.id} {principle.title}")
        actual_anchor = file.index_ids.get(principle.id)
        if actual_anchor is None or actual_anchor == expected_anchor:
            continue
        problems.append(f"{display_path(file.path)}: index links {principle.id} to #{actual_anchor}, section is #{expected_anchor}")
    return problems


def check_sections_under_matching_level(file: PrincipleFile) -> list[str]:
    problems: list[str] = []
    for principle in file.principles:
        level_in_id = principle.id[1]
        if principle.level_of_section == level_in_id:
            continue
        problems.append(f"{display_path(file.path)}: {principle.id} sits under level {principle.level_of_section or 'none'}, its ID says {level_in_id}")
    return problems


def check_links_resolve(file: PrincipleFile, files_by_path: dict[Path, PrincipleFile]) -> list[str]:
    problems: list[str] = []
    for line in file.lines:
        for link in LINK_WITH_ANCHOR.finditer(line):
            target_path = (file.path.parent / link.group("target")).resolve() if link.group("target") else file.path
            target = files_by_path.get(target_path)
            if target is None:
                problems.append(f"{display_path(file.path)}: link to unknown file {link.group('target')}")
                continue
            if link.group("anchor") in target.anchors:
                continue
            problems.append(f"{display_path(file.path)}: #{link.group('anchor')} does not exist in {display_path(target.path)}")
    return problems


def check_back_to_index_links(file: PrincipleFile) -> list[str]:
    problems: list[str] = []
    for principle in file.principles:
        if principle.last_line in BACK_TO_INDEX_LINKS:
            continue
        problems.append(f"{display_path(file.path)}: {principle.id} does not end with a link back to the index")
    return problems


def check_retired_table(lines: list[str], current_ids: set[str]) -> list[str]:
    problems: list[str] = []
    for retired_id, successor in collect_retired_rows(lines):
        if retired_id in current_ids:
            problems.append(f"retired table: {retired_id} is retired but still has a section")
        if successor == NO_SUCCESSOR or successor in current_ids:
            continue
        problems.append(f"retired table: successor {successor} of {retired_id} does not exist")
    return problems


def run_all_checks(files: list[PrincipleFile], linking_files: list[PrincipleFile]) -> list[str]:
    problems: list[str] = []
    problems.extend(check_id_format(files))
    problems.extend(check_ids_unique(files))
    files_by_path = {file.path: file for file in files + linking_files}
    for file in files:
        problems.extend(check_index_matches_sections(file))
        problems.extend(check_sections_under_matching_level(file))
        problems.extend(check_links_resolve(file, files_by_path))
        problems.extend(check_back_to_index_links(file))
    for linking_file in linking_files:
        problems.extend(check_links_resolve(linking_file, files_by_path))
    current_ids = {principle.id for file in files for principle in file.principles}
    retired_table_lines = RETIRED_TABLE_FILE.read_text(encoding="utf-8").splitlines()
    problems.extend(check_retired_table(retired_table_lines, current_ids))
    return problems


def main() -> int:
    files = [load_principle_file(path) for path in PRINCIPLE_FILES]
    linking_files = [load_principle_file(path) for path in FILES_LINKING_TO_PRINCIPLES]
    problems = run_all_checks(files, linking_files)
    for problem in problems:
        print(problem)
    principle_count = sum(len(file.principles) for file in files)
    print(f"{principle_count} principles checked, {len(problems)} problems")
    if problems:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
