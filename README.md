# plain-language

![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)

An agent skill that applies plain-language principles to an AI coding
agent's chat replies and to any prose it writes, edits, reviews, or
translates. A skill is a directory of instructions an agent loads on demand,
following the [Agent Skills specification](https://agentskills.io/specification).

The principles come from plain-language guidance and editorial practice,
selected and adjusted for that work. They cover the way an agent changes
existing text as well as the text it produces, and they leave out
conventional writing advice that backfires when agents follow it. They do
not claim compliance with a formal plain-language standard.

This repository also holds the tools that maintain the skill. One runs a
prompt with and without the skill and shows the replies side by side. Another records an unnatural expression that a reader noticed in a
reply, with the prompt that produced it, so that the maintainers can fix
the principles.

## Contents

| Path | Description |
| --- | --- |
| [plain-language/SKILL.md](plain-language/SKILL.md) | The shared principles, each with an ID, application guidance, a reason, and an example. |
| [plain-language/references/english.md](plain-language/references/english.md) | Principles for English text that the agent produces or reviews. |
| [plain-language/references/japanese.md](plain-language/references/japanese.md) | Principles for Japanese text that the agent produces or reviews. |
| [plain-language-compare/](plain-language-compare/SKILL.md) | Skill that runs one prompt with and without the plain-language skill, across versions of it, or across models, and shows the replies side by side. |
| plain-language-report/ | Skill that records an unnatural expression noticed in a reply as a report, by asking the reader a few questions. Planned. |
| evals/ | The comparisons and reports worth keeping. They serve as the regression suite and as evidence of what the skill does. Planned. |
| [scripts/validate.py](scripts/validate.py) | Checks that the principle files agree with themselves: IDs, index rows, levels, links, and the retired table. |

## Installation

Install the skill with [GitHub CLI](https://cli.github.com/)'s `gh skill`:

```sh
gh skill install hainet50b/plain-language plain-language --agent universal --scope user
```

Pass `--agent claude-code` (or another agent) for agents that load skills only
from a directory of their own. See `gh skill install --help` for the full list.
To update the skill, run `gh skill update plain-language`.

## How the principles are organized

Every principle has an ID such as `P302` or `J601`. The letter names the
language the principle applies to, and the first digit names the level of
language the principle works at. The section
[Maintain the principles](plain-language/SKILL.md#maintain-the-principles)
in SKILL.md defines the letters and the levels.

## License

Licensed under either of

 * Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <http://www.apache.org/licenses/LICENSE-2.0>)
 * MIT license ([LICENSE-MIT](LICENSE-MIT) or <http://opensource.org/licenses/MIT>)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
