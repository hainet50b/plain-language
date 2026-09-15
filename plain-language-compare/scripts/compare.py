"""Run one prompt under several sets of principles and models, and show the replies side by side.

Usage: python scripts/compare.py [PROMPT] [options]
Run with --help for the options.
Exit code 0 when every sample succeeded, 1 when some sample failed,
2 on a usage or resolution error.
"""

import argparse
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

SKILL_DIRECTORY = Path(__file__).resolve().parent.parent
VIEWER_TEMPLATE_FILE = SKILL_DIRECTORY / "assets" / "viewer.html"
MARKED_FILE = SKILL_DIRECTORY / "assets" / "marked.umd.js"

PRINCIPLES_SKILL_NAME = "plain-language"
PRINCIPLES_DIRECTORY_IN_REPOSITORY = "plain-language"
PRINCIPLES_MAIN_FILE = "SKILL.md"
COMPARISON_FORMAT_VERSION = 2

# The Agent Skills specification places a skill's reference files under
# references/, so only SKILL.md and that directory count as principles.
PRINCIPLES_REFERENCES_DIRECTORY = "references"
# A hidden directory in the home directory, like ~/.docker: the same path on
# every system, and one that a script started by an agent can write to.
DATA_DIRECTORY_NAME = ".plain-language"
INSTALLED_SKILL_PARENTS = [
    Path(".claude") / "skills",
    Path(".agents") / "skills",
    Path.home() / ".claude" / "skills",
    Path.home() / ".agents" / "skills",
]

DEFAULT_PRINCIPLES_SETS = ["none", "installed"]
AGENT_NAMES = ["claude"]
DEFAULT_AGENT = "claude"
# Claude Code itself calls the model a user has configured "default".
DEFAULT_MODEL_LABEL = "default"
DEFAULT_EFFORT = "high"
EFFORT_LEVELS = ["low", "medium", "high", "xhigh", "max"]
DEFAULT_SAMPLES = 1
# Claude Code pools rate limits across sessions; reports say four or more
# concurrent sessions start to hit them.
DEFAULT_PARALLEL = 3
SLUG_MAX_CHARACTERS = 40
# Keeps the prompt line of the plan within an 80-column terminal, indent
# included, even when every character is full-width.
PLAN_PROMPT_MAX_CHARACTERS = 40
# Windows limits a whole path to 260 characters, so a file name derived from
# a name such as "dir:C:\..." is cut and made unique with a hash instead.
FILE_NAME_MAX_CHARACTERS = 40
FILE_NAME_HASH_CHARACTERS = 8
SHORT_COMMIT_CHARACTERS = 7

EXIT_SUCCESS = 0
EXIT_SAMPLE_FAILED = 1
EXIT_USAGE = 2

# matches "## Prompt" and "## Source" (a level-two heading naming a report section)
REPORT_SECTION_HEADING = re.compile(r"^## (?P<title>.+?)\s*$")
# matches "---" (a frontmatter fence)
FRONTMATTER_FENCE = re.compile(r"^---\s*$")
# matches "2.1.267" in "2.1.267 (Claude Code)"
CLAUDE_VERSION = re.compile(r"^(?P<version>\d+\.\d+\.\d+)")
# matches ":" and "\" in "dir:C:\work\principles" (characters unsafe in a file name); does not match "c34ccd4" or "opus"
UNSAFE_FILE_NAME_CHARACTER = re.compile(r"[^A-Za-z0-9._-]")


class UsageError(Exception):
    pass


@dataclass
class Prompt:
    text: str
    source: str | None
    report_file: str | None

    def message_text(self) -> str:
        if self.source is None:
            return self.text
        return self.text.rstrip() + "\n\n" + self.source


@dataclass
class PrincipleFile:
    path: str
    content: str

    def sha256(self) -> str:
        return sha256_of_text(self.content)


@dataclass
class Principles:
    name: str
    origin: dict
    files: list[PrincipleFile]

    def has_text(self) -> bool:
        return len(self.files) > 0

    def text(self) -> str:
        return concatenate_principle_files(self.files)


@dataclass
class ModelChoice:
    label: str
    requested: str | None


@dataclass
class SampleRequest:
    principles: Principles
    model_choice: ModelChoice
    index: int
    principles_text_file: Path | None


@dataclass
class Sample:
    principles_name: str
    model_label: str
    index: int
    file: str | None = None
    model: str | None = None
    stop_reason: str | None = None
    is_error: bool = False
    error: str | None = None
    duration_ms: int | None = None
    duration_api_ms: int | None = None
    cost_usd: float | None = None
    usage: dict = field(default_factory=dict)
    session_id: str | None = None
    text: str = ""


def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_name_from(name: str) -> str:
    safe_name = UNSAFE_FILE_NAME_CHARACTER.sub("-", name)
    if len(safe_name) <= FILE_NAME_MAX_CHARACTERS:
        return safe_name
    kept_length = FILE_NAME_MAX_CHARACTERS - FILE_NAME_HASH_CHARACTERS - 1
    name_hash = sha256_of_text(name)[:FILE_NAME_HASH_CHARACTERS]
    return f"{safe_name[:kept_length].rstrip('-')}-{name_hash}"


def default_data_directory() -> Path:
    return Path.home() / DATA_DIRECTORY_NAME


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="compare.py",
        description=(
            "Run one prompt under several sets of principles and models, and show the replies side by side.\n"
            "Each combination of a set of principles and a model runs --samples times."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Sets of principles:\n"
            "  none        no principles; the baseline\n"
            "  installed   the plain-language skill installed on this machine\n"
            "  worktree    the principle files on disk in the checkout, uncommitted edits included\n"
            "  <git ref>   the principle files as committed at that ref, such as HEAD or a commit\n"
            "  dir:PATH    a skill directory: its SKILL.md and the files under references/\n"
            "worktree and git refs need --repo, or a current directory that is the checkout."
        ),
    )
    prompt_group = parser.add_argument_group("prompt")
    prompt_group.add_argument("prompt", nargs="?", help="the prompt; stdin when omitted")
    prompt_group.add_argument("--prompt-file", metavar="FILE", help="a file holding the prompt")
    prompt_group.add_argument("--source-file", metavar="FILE", help="a file holding the source text, such as a text to edit or translate")
    prompt_group.add_argument("--report-file", metavar="FILE", help="a report file")

    principles_group = parser.add_argument_group("principles")
    principles_group.add_argument("--principles", action="append", metavar="SET", help=f"a set of principles for the model to read; repeatable; default: {', '.join(DEFAULT_PRINCIPLES_SETS)}")
    principles_group.add_argument("--repo", metavar="DIR", help="the plain-language checkout for worktree and git refs")

    agent_group = parser.add_argument_group("agent")
    agent_group.add_argument("--agent", default=DEFAULT_AGENT, choices=AGENT_NAMES, help=f"the agent that answers the prompt; default {DEFAULT_AGENT}")
    agent_group.add_argument("--model", action="append", metavar="ID", help="a model alias or ID for the agent; repeatable; default: the model the agent uses")
    agent_group.add_argument("--effort", default=DEFAULT_EFFORT, choices=EFFORT_LEVELS, help=f"the effort level; default {DEFAULT_EFFORT}")

    sampling_group = parser.add_argument_group("sampling")
    sampling_group.add_argument("--samples", type=int, default=DEFAULT_SAMPLES, metavar="N", help=f"the number of samples per set of principles and model; default {DEFAULT_SAMPLES}")
    sampling_group.add_argument("--parallel", type=int, default=DEFAULT_PARALLEL, metavar="N", help=f"the number of agent processes running at once; default {DEFAULT_PARALLEL}")

    output_group = parser.add_argument_group("output")
    output_group.add_argument("--out", metavar="DIR", help="the directory to write the comparison to; default: ~/.plain-language/comparisons")
    output_group.add_argument("--name", metavar="SLUG", help="the name of the comparison; default: taken from the prompt")
    output_group.add_argument("--open", action="store_true", help="open index.html in the browser when done")
    output_group.add_argument("--dry-run", action="store_true", help="print what would run, without calling the model")
    return parser.parse_args(argv)


def read_prompt(arguments: argparse.Namespace) -> Prompt:
    prompt_sources_given = [
        arguments.prompt is not None,
        arguments.prompt_file is not None,
        arguments.report_file is not None,
    ]
    if sum(prompt_sources_given) > 1:
        raise UsageError("give the prompt in one way only: as an argument, with --prompt-file, or with --report-file")
    if arguments.report_file is not None:
        return read_prompt_from_report(Path(arguments.report_file))
    text = read_prompt_text(arguments)
    source = read_text_file(Path(arguments.source_file)) if arguments.source_file else None
    return Prompt(text=text, source=source, report_file=None)


def read_prompt_text(arguments: argparse.Namespace) -> str:
    if arguments.prompt is not None:
        text = arguments.prompt
    elif arguments.prompt_file is not None:
        text = read_text_file(Path(arguments.prompt_file))
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        raise UsageError("no prompt given; pass it as an argument, with --prompt-file, --report-file, or on stdin")
    if text.strip() == "":
        raise UsageError("the prompt is empty")
    return text.strip()


def read_prompt_from_report(report_file: Path) -> Prompt:
    sections = read_report_sections(read_text_file(report_file))
    if "Prompt" not in sections or sections["Prompt"].strip() == "":
        raise UsageError(f"{report_file} has no '## Prompt' section")
    source = sections.get("Source")
    if source is not None and source.strip() == "":
        source = None
    return Prompt(text=sections["Prompt"].strip(), source=source, report_file=str(report_file))


def read_report_sections(text: str) -> dict[str, str]:
    lines = skip_frontmatter(text.splitlines())
    sections: dict[str, str] = {}
    current_title = None
    current_lines: list[str] = []
    for line in lines:
        heading = REPORT_SECTION_HEADING.match(line)
        if heading is None:
            current_lines.append(line)
            continue
        if current_title is not None:
            sections[current_title] = "\n".join(current_lines).strip()
        current_title = heading.group("title")
        current_lines = []
    if current_title is not None:
        sections[current_title] = "\n".join(current_lines).strip()
    return sections


def skip_frontmatter(lines: list[str]) -> list[str]:
    if not lines or not FRONTMATTER_FENCE.match(lines[0]):
        return lines
    for line_number in range(1, len(lines)):
        if FRONTMATTER_FENCE.match(lines[line_number]):
            return lines[line_number + 1:]
    return lines


def read_text_file(path: Path) -> str:
    if not path.is_file():
        raise UsageError(f"{path} is not a file")
    return path.read_text(encoding="utf-8")


def resolve_principles_list(names: list[str], repository: Path | None) -> list[Principles]:
    require_unique(names, "sets of principles")
    return [resolve_principles(name, repository) for name in names]


def require_unique(values: list[str], kind: str) -> None:
    if len(set(values)) != len(values):
        raise UsageError(f"{kind} must be unique; got {', '.join(values)}")


def resolve_principles(name: str, repository: Path | None) -> Principles:
    if name == "none":
        return Principles(name=name, origin={"kind": "none"}, files=[])
    if name == "installed":
        return resolve_installed_principles(name)
    if name.startswith("dir:"):
        return resolve_directory_principles(name, Path(name[len("dir:"):]))
    if repository is None:
        raise UsageError(f"the set of principles '{name}' needs the repository; pass --repo or run in the checkout")
    if name == "worktree":
        return resolve_worktree_principles(name, repository)
    return resolve_git_ref_principles(name, repository)


def resolve_installed_principles(name: str) -> Principles:
    skill_directory = find_installed_skill_directory()
    if skill_directory is None:
        searched = ", ".join(str(parent / PRINCIPLES_SKILL_NAME) for parent in INSTALLED_SKILL_PARENTS)
        raise UsageError(f"the {PRINCIPLES_SKILL_NAME} skill is not installed; looked in {searched}")
    origin = {"kind": "installed", "path": str(skill_directory)}
    return Principles(name=name, origin=origin, files=read_principle_files_from_directory(skill_directory))


def find_installed_skill_directory() -> Path | None:
    for parent in INSTALLED_SKILL_PARENTS:
        candidate = parent / PRINCIPLES_SKILL_NAME
        if (candidate / PRINCIPLES_MAIN_FILE).is_file():
            return candidate.resolve()
    return None


def resolve_directory_principles(name: str, directory: Path) -> Principles:
    if not (directory / PRINCIPLES_MAIN_FILE).is_file():
        raise UsageError(f"{directory} has no {PRINCIPLES_MAIN_FILE}")
    origin = {"kind": "directory", "path": str(directory.resolve())}
    return Principles(name=name, origin=origin, files=read_principle_files_from_directory(directory))


def resolve_worktree_principles(name: str, repository: Path) -> Principles:
    principles_directory = repository / PRINCIPLES_DIRECTORY_IN_REPOSITORY
    if not (principles_directory / PRINCIPLES_MAIN_FILE).is_file():
        raise UsageError(f"{repository} has no {PRINCIPLES_DIRECTORY_IN_REPOSITORY}/{PRINCIPLES_MAIN_FILE}")
    head_commit = run_git(repository, ["rev-parse", "HEAD"]).strip()
    status = run_git(repository, ["status", "--porcelain", "--", PRINCIPLES_DIRECTORY_IN_REPOSITORY])
    origin = {
        "kind": "worktree",
        "path": str(principles_directory.resolve()),
        "head": head_commit,
        "has_uncommitted_changes": status.strip() != "",
    }
    return Principles(name=name, origin=origin, files=read_principle_files_from_directory(principles_directory))


def resolve_git_ref_principles(name: str, repository: Path) -> Principles:
    commit = run_git(repository, ["rev-parse", "--verify", "--quiet", f"{name}^{{commit}}"]).strip()
    if commit == "":
        raise UsageError(f"'{name}' is not a set of principles or a git ref in {repository}")
    main_file_in_repository = f"{PRINCIPLES_DIRECTORY_IN_REPOSITORY}/{PRINCIPLES_MAIN_FILE}"
    references_in_repository = f"{PRINCIPLES_DIRECTORY_IN_REPOSITORY}/{PRINCIPLES_REFERENCES_DIRECTORY}"
    listed = run_git(repository, ["ls-tree", "-r", "--name-only", commit, "--", main_file_in_repository, references_in_repository])
    paths_in_repository = [line for line in listed.splitlines() if line.endswith(".md")]
    files = []
    for path_in_repository in order_principle_paths(paths_in_repository, PRINCIPLES_DIRECTORY_IN_REPOSITORY + "/"):
        content = run_git(repository, ["show", f"{commit}:{path_in_repository}"])
        relative_path = path_in_repository[len(PRINCIPLES_DIRECTORY_IN_REPOSITORY) + 1:]
        files.append(PrincipleFile(path=relative_path, content=content))
    if not files:
        raise UsageError(f"{name} has no principle files under {PRINCIPLES_DIRECTORY_IN_REPOSITORY}/")
    origin = {"kind": "git", "repository": str(repository.resolve()), "commit": commit}
    return Principles(name=name, origin=origin, files=files)


def run_git(repository: Path, git_arguments: list[str]) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository)] + git_arguments,
        capture_output=True, text=True, encoding="utf-8",
    )
    if completed.returncode != 0 and "--quiet" not in git_arguments:
        raise UsageError(f"git {' '.join(git_arguments)} failed in {repository}: {completed.stderr.strip()}")
    return completed.stdout


def read_principle_files_from_directory(directory: Path) -> list[PrincipleFile]:
    paths = [PRINCIPLES_MAIN_FILE]
    references_directory = directory / PRINCIPLES_REFERENCES_DIRECTORY
    if references_directory.is_dir():
        paths += [path.relative_to(directory).as_posix() for path in references_directory.rglob("*.md")]
    files = []
    for relative_path in order_principle_paths(paths, ""):
        content = (directory / relative_path).read_text(encoding="utf-8")
        files.append(PrincipleFile(path=relative_path, content=content))
    return files


def order_principle_paths(paths: list[str], prefix: str) -> list[str]:
    main_file = prefix + PRINCIPLES_MAIN_FILE
    ordered = [path for path in paths if path == main_file]
    ordered += sorted(path for path in paths if path != main_file)
    return ordered


def concatenate_principle_files(files: list[PrincipleFile]) -> str:
    parts = []
    for principle_file in files:
        parts.append(f"<!-- {PRINCIPLES_SKILL_NAME} file: {principle_file.path} -->\n\n{principle_file.content.rstrip()}\n")
    return "\n".join(parts)


def resolve_repository(repository_argument: str | None) -> Path | None:
    repository = Path(repository_argument or ".")
    if (repository / PRINCIPLES_DIRECTORY_IN_REPOSITORY / PRINCIPLES_MAIN_FILE).is_file():
        return repository
    if repository_argument is None:
        return None
    raise UsageError(f"{repository} is not a plain-language checkout")


def resolve_model_choices(model_arguments: list[str] | None) -> list[ModelChoice]:
    if not model_arguments:
        return [ModelChoice(label=DEFAULT_MODEL_LABEL, requested=None)]
    require_unique(model_arguments, "models")
    return [ModelChoice(label=model_argument, requested=model_argument) for model_argument in model_arguments]


def find_agent_executable(agent_name: str) -> str:
    executable = shutil.which(agent_name)
    if executable is None:
        raise UsageError(f"the '{agent_name}' command is not on PATH")
    return executable


def read_agent_version(agent_executable: str) -> str | None:
    completed = subprocess.run([agent_executable, "--version"], capture_output=True, text=True, encoding="utf-8")
    match = CLAUDE_VERSION.match(completed.stdout.strip())
    if match is None:
        return None
    return match.group("version")


def build_claude_command(agent_executable: str, model_choice: ModelChoice, effort: str, principles_text_file: Path | None) -> list[str]:
    command = [
        agent_executable, "-p",
        "--tools", "",
        "--effort", effort,
        "--output-format", "json",
        "--no-session-persistence",
    ]
    if model_choice.requested is not None:
        command += ["--model", model_choice.requested]
    if principles_text_file is not None:
        command += ["--append-system-prompt-file", str(principles_text_file)]
    return command


def run_sample(request: SampleRequest, message_text: str, agent_executable: str, effort: str) -> Sample:
    sample = Sample(principles_name=request.principles.name, model_label=request.model_choice.label, index=request.index)
    command = build_claude_command(agent_executable, request.model_choice, effort, request.principles_text_file)
    completed = subprocess.run(command, input=message_text, capture_output=True, text=True, encoding="utf-8")
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        sample.is_error = True
        sample.error = describe_process_failure(completed)
        return sample
    fill_sample_from_result(sample, result)
    return sample


def describe_process_failure(completed: subprocess.CompletedProcess) -> str:
    stderr_tail = completed.stderr.strip()[-2000:]
    stdout_tail = completed.stdout.strip()[-500:]
    return f"the agent exited with {completed.returncode}; stderr: {stderr_tail}; stdout: {stdout_tail}"


def fill_sample_from_result(sample: Sample, result: dict) -> None:
    sample.is_error = bool(result.get("is_error", False))
    sample.stop_reason = result.get("stop_reason")
    sample.duration_ms = result.get("duration_ms")
    sample.duration_api_ms = result.get("duration_api_ms")
    sample.cost_usd = result.get("total_cost_usd")
    sample.session_id = result.get("session_id")
    sample.usage = select_usage_fields(result.get("usage", {}))
    sample.model = first_model_used(result.get("modelUsage", {}))
    result_text = result.get("result")
    if sample.is_error:
        sample.error = str(result_text)
        return
    sample.text = result_text if isinstance(result_text, str) else json.dumps(result_text, ensure_ascii=False)


def select_usage_fields(usage: dict) -> dict:
    field_names = ["input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"]
    return {name: usage.get(name) for name in field_names if name in usage}


def first_model_used(model_usage: dict) -> str | None:
    for model_id in model_usage:
        return model_id
    return None


def run_all_samples(requests: list[SampleRequest], message_text: str, agent_executable: str, effort: str, parallel: int) -> list[Sample]:
    # The first sample of each set of principles and model creates the prompt
    # cache that the later samples read, so those run in a phase of their own.
    first_samples = [request for request in requests if request.index == 1]
    later_samples = [request for request in requests if request.index != 1]
    samples = []
    samples += run_phase(first_samples, message_text, agent_executable, effort, parallel)
    samples += run_phase(later_samples, message_text, agent_executable, effort, parallel)
    return samples


def run_phase(requests: list[SampleRequest], message_text: str, agent_executable: str, effort: str, parallel: int) -> list[Sample]:
    if not requests:
        return []

    def run_one(request: SampleRequest) -> Sample:
        return run_sample(request, message_text, agent_executable, effort)

    samples = []
    with ThreadPoolExecutor(max_workers=parallel) as executor:
        for sample in executor.map(run_one, requests):
            report_sample_progress(sample)
            samples.append(sample)
    return samples


def report_sample_progress(sample: Sample) -> None:
    cell = f"{sample.principles_name} under {sample.model_label}"
    if sample.is_error:
        print(f"  {cell} {sample.index}: failed: {sample.error}", file=sys.stderr)
        return
    seconds = (sample.duration_ms or 0) / 1000
    cost = sample.cost_usd or 0.0
    print(f"  {cell} {sample.index}: done in {seconds:.1f} s, ${cost:.3f}", file=sys.stderr)


def slug_from_prompt(prompt_text: str) -> str:
    first_line = prompt_text.strip().splitlines()[0]
    characters = []
    for character in first_line:
        characters.append(character if character.isalnum() else "-")
    slug = re.sub(r"-+", "-", "".join(characters)).strip("-").lower()
    if slug == "":
        return "comparison"
    return slug[:SLUG_MAX_CHARACTERS].rstrip("-")


def make_comparison_directory(out_directory: Path, slug: str, created_at: datetime.datetime) -> Path:
    base_name = f"{created_at.strftime('%Y-%m-%d')}-{slug}"
    comparison_directory = out_directory / base_name
    suffix = 2
    while comparison_directory.exists():
        comparison_directory = out_directory / f"{base_name}-{suffix}"
        suffix += 1
    comparison_directory.mkdir(parents=True)
    return comparison_directory


def write_prompt_files(prompt: Prompt, comparison_directory: Path) -> dict:
    prompt_directory = comparison_directory / "prompt"
    prompt_directory.mkdir(exist_ok=True)
    (prompt_directory / "prompt.md").write_text(prompt.text, encoding="utf-8", newline="\n")
    described = {"file": "prompt/prompt.md", "source_file": None, "report": prompt.report_file}
    if prompt.source is not None:
        (prompt_directory / "source.md").write_text(prompt.source, encoding="utf-8", newline="\n")
        described["source_file"] = "prompt/source.md"
    return described


def write_principles_texts(principles_list: list[Principles], comparison_directory: Path) -> dict[str, Path | None]:
    text_files: dict[str, Path | None] = {}
    for principles in principles_list:
        if not principles.has_text():
            text_files[principles.name] = None
            continue
        principles_directory = comparison_directory / "principles"
        principles_directory.mkdir(exist_ok=True)
        text_file = principles_directory / f"{file_name_from(principles.name)}.md"
        text_file.write_text(principles.text(), encoding="utf-8", newline="\n")
        text_files[principles.name] = text_file
    return text_files


def sample_relative_file(sample: Sample) -> str:
    cell_directory = f"{file_name_from(sample.principles_name)}.{file_name_from(sample.model_label)}"
    return f"samples/{cell_directory}/{sample.index}.md"


def write_sample_texts(samples: list[Sample], comparison_directory: Path) -> None:
    for sample in samples:
        if sample.is_error:
            continue
        relative_file = sample_relative_file(sample)
        sample_file = comparison_directory / relative_file
        sample_file.parent.mkdir(parents=True, exist_ok=True)
        sample_file.write_text(sample.text, encoding="utf-8", newline="\n")
        sample.file = relative_file


def describe_principles(principles: Principles, text_file: Path | None, comparison_directory: Path) -> dict:
    described = {
        "name": principles.name,
        "origin": principles.origin,
        "files": [{"path": principle_file.path, "sha256": principle_file.sha256()} for principle_file in principles.files],
        "text_file": None,
        "text_sha256": None,
    }
    if text_file is not None:
        described["text_file"] = text_file.relative_to(comparison_directory).as_posix()
        described["text_sha256"] = sha256_of_text(principles.text())
    return described


def describe_sample(sample: Sample) -> dict:
    return {
        "principles": sample.principles_name,
        "model_label": sample.model_label,
        "index": sample.index,
        "file": sample.file,
        "model": sample.model,
        "stop_reason": sample.stop_reason,
        "is_error": sample.is_error,
        "error": sample.error,
        "duration_ms": sample.duration_ms,
        "duration_api_ms": sample.duration_api_ms,
        "cost_usd": sample.cost_usd,
        "usage": sample.usage,
        "session_id": sample.session_id,
    }


def build_comparison(prompt_files: dict, principles_list: list[Principles], text_files: dict[str, Path | None], model_choices: list[ModelChoice], samples: list[Sample], comparison_directory: Path, created_at: datetime.datetime, agent_name: str, agent_version: str | None, effort: str) -> dict:
    return {
        "format": COMPARISON_FORMAT_VERSION,
        "created_at": created_at.isoformat(timespec="seconds"),
        "prompt": prompt_files,
        "principles": [describe_principles(principles, text_files[principles.name], comparison_directory) for principles in principles_list],
        "agent": {"name": agent_name, "version": agent_version},
        "models": [{"label": choice.label, "requested": choice.requested} for choice in model_choices],
        "effort": effort,
        "samples": [describe_sample(sample) for sample in samples],
    }


def write_comparison_json(comparison: dict, comparison_directory: Path) -> None:
    comparison_text = json.dumps(comparison, ensure_ascii=False, indent=2) + "\n"
    (comparison_directory / "comparison.json").write_text(comparison_text, encoding="utf-8", newline="\n")


def render_index_html(comparison: dict, prompt: Prompt, samples: list[Sample], comparison_directory: Path) -> Path:
    template = VIEWER_TEMPLATE_FILE.read_text(encoding="utf-8")
    marked_script = MARKED_FILE.read_text(encoding="utf-8")
    prompt_texts = {"prompt": prompt.text, "source": prompt.source}
    html = template.replace("__MARKED_JS__", marked_script)
    html = html.replace("__COMPARISON_JSON__", json_for_script(comparison))
    html = html.replace("__PROMPT_JSON__", json_for_script(prompt_texts))
    html = html.replace("__SAMPLES_JSON__", json_for_script(nest_sample_texts(samples)))
    index_file = comparison_directory / "index.html"
    index_file.write_text(html, encoding="utf-8", newline="\n")
    return index_file


def nest_sample_texts(samples: list[Sample]) -> dict:
    # Nested by model label, then principles name, then index, so that names
    # can contain any character without a separator to collide with.
    nested: dict = {}
    for sample in samples:
        by_principles = nested.setdefault(sample.model_label, {})
        by_index = by_principles.setdefault(sample.principles_name, {})
        by_index[str(sample.index)] = sample.text
    return nested


def json_for_script(value) -> str:
    # A literal "</script>" inside the JSON would end the script element early.
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def shorten_prompt_for_plan(prompt_text: str) -> str:
    lines = prompt_text.strip().splitlines()
    first_line = lines[0]
    if len(first_line) <= PLAN_PROMPT_MAX_CHARACTERS and len(lines) == 1:
        return first_line
    return first_line[:PLAN_PROMPT_MAX_CHARACTERS].rstrip() + "…"


def describe_origin_for_plan(principles: Principles) -> str:
    origin = principles.origin
    kind = origin["kind"]
    if kind == "none":
        return "no principles"
    size = count_with_noun(len(principles.text()), "character")
    if kind == "worktree":
        edits = ", with uncommitted edits" if origin["has_uncommitted_changes"] else ""
        return f"{size}, {origin['path']}{edits}"
    if kind == "git":
        return f"{size}, {origin['repository']} at {origin['commit'][:SHORT_COMMIT_CHARACTERS]}"
    return f"{size}, {origin['path']}"


def print_plan(prompt: Prompt, principles_list: list[Principles], model_choices: list[ModelChoice], samples_per_cell: int, output_description: str, agent_name: str, effort: str) -> None:
    lines = ["Prompt:", f"  {shorten_prompt_for_plan(prompt.text)}"]
    if prompt.source is not None:
        lines.append(f"  with a source of {count_with_noun(len(prompt.source), 'character')}")
    lines.append("Principles:")
    for principles in principles_list:
        lines.append(f"  {principles.name}: {describe_origin_for_plan(principles)}")
    lines.append(f"Agent: {agent_name}")
    lines.append(f"Models: {', '.join(choice.label for choice in model_choices)}")
    lines.append(f"Effort: {effort}")
    total_calls = len(principles_list) * len(model_choices) * samples_per_cell
    lines.append(f"Samples: {samples_per_cell} per set of principles and model, {count_with_noun(total_calls, 'model call')}")
    lines.append(f"Output: {output_description}")
    for line in lines:
        print(line, file=sys.stderr)


def print_summary(samples: list[Sample], elapsed_seconds: float) -> None:
    failed_count = sum(1 for sample in samples if sample.is_error)
    total_cost = sum(sample.cost_usd or 0.0 for sample in samples)
    print("", file=sys.stderr)
    print(f"Summary: {count_with_noun(len(samples), 'sample')}, {failed_count} failed, ${total_cost:.2f}, {elapsed_seconds:.0f} s", file=sys.stderr)
    if failed_count > 0:
        print(f"FAILED: {failed_count} of {count_with_noun(len(samples), 'sample')} failed", file=sys.stderr)
        return
    print("OK", file=sys.stderr)


def count_with_noun(count: int, noun: str) -> str:
    if count == 1:
        return f"1 {noun}"
    return f"{count} {noun}s"


def main(argv: list[str]) -> int:
    arguments = parse_arguments(argv)
    if arguments.samples < 1:
        raise UsageError("--samples must be at least 1")
    if arguments.parallel < 1:
        raise UsageError("--parallel must be at least 1")

    prompt = read_prompt(arguments)
    repository = resolve_repository(arguments.repo)
    principles_list = resolve_principles_list(arguments.principles or DEFAULT_PRINCIPLES_SETS, repository)
    model_choices = resolve_model_choices(arguments.model)
    out_directory = Path(arguments.out) if arguments.out else default_data_directory() / "comparisons"

    if arguments.dry_run:
        print_plan(prompt, principles_list, model_choices, arguments.samples, f"a new directory under {out_directory}", arguments.agent, arguments.effort)
        return EXIT_SUCCESS

    agent_executable = find_agent_executable(arguments.agent)
    agent_version = read_agent_version(agent_executable)
    created_at = datetime.datetime.now().astimezone()
    comparison_directory = make_comparison_directory(out_directory, arguments.name or slug_from_prompt(prompt.text), created_at)
    print_plan(prompt, principles_list, model_choices, arguments.samples, str(comparison_directory), arguments.agent, arguments.effort)
    prompt_files = write_prompt_files(prompt, comparison_directory)
    text_files = write_principles_texts(principles_list, comparison_directory)

    requests = []
    for model_choice in model_choices:
        for principles in principles_list:
            for index in range(1, arguments.samples + 1):
                requests.append(SampleRequest(principles=principles, model_choice=model_choice, index=index, principles_text_file=text_files[principles.name]))
    print("", file=sys.stderr)
    print("Running:", file=sys.stderr)
    started = time.monotonic()
    samples = run_all_samples(requests, prompt.message_text(), agent_executable, arguments.effort, arguments.parallel)
    elapsed_seconds = time.monotonic() - started

    write_sample_texts(samples, comparison_directory)
    comparison = build_comparison(prompt_files, principles_list, text_files, model_choices, samples, comparison_directory, created_at, arguments.agent, agent_version, arguments.effort)
    write_comparison_json(comparison, comparison_directory)
    index_file = render_index_html(comparison, prompt, samples, comparison_directory)
    print_summary(samples, elapsed_seconds)
    print(str(comparison_directory))
    if arguments.open:
        webbrowser.open(index_file.resolve().as_uri())

    if any(sample.is_error for sample in samples):
        return EXIT_SAMPLE_FAILED
    return EXIT_SUCCESS


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        sys.exit(main(sys.argv[1:]))
    except UsageError as error:
        print(f"compare.py: {error}", file=sys.stderr)
        sys.exit(EXIT_USAGE)
