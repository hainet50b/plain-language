![plain-language](assets/banner.png)

![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)

An agent skill that helps an AI coding agent say plainly what matters
most to the reader at that moment. It applies to the explanations,
reports, and documents the agent writes, and to any text it edits,
reviews, or translates. A skill is a directory of instructions an agent
loads on demand, following the
[Agent Skills specification](https://agentskills.io/specification).

Current models write sentences that are correct one by one, yet the point
often fails to come through. Hedges, qualifications, and asides pile up
around it, terms come from outside the reader's field, and an edit changes
meaning nobody asked to change. The skill aims at that gap.

This repository also holds the tools that maintain the skill. One runs a
prompt with and without the skill and shows the replies side by side.
Another records an expression that felt unnatural to a reader as a report,
with the prompt that produces it, so that the maintainers can fix the
principles.

## Contents

| Path | Description |
| --- | --- |
| [plain-language/SKILL.md](plain-language/SKILL.md) | The shared principles, each with an ID, application guidance, a reason, and an example. |
| [plain-language/references/english.md](plain-language/references/english.md) | Principles for English text that the agent produces or reviews. |
| [plain-language/references/japanese.md](plain-language/references/japanese.md) | Principles for Japanese text that the agent produces or reviews. |
| [plain-language-compare/](plain-language-compare/SKILL.md) | Skill that runs one prompt with and without the plain-language skill, across versions of it, or across models, and shows the replies side by side. |
| [plain-language-report/](plain-language-report/SKILL.md) | Skill that records an expression that feels unnatural to a reader as a report, with the prompt that produces it, by asking the reader what felt unnatural. |
| [evals/](evals/README.md) | The reports and comparisons worth keeping. They serve as the regression suite and as evidence of what the skill does. |
| [MAINTAINING.md](MAINTAINING.md) | How principle IDs are assigned, and the record of retired IDs. The agent does not read it. |
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

Every principle has an ID such as `P501` or `J601`. The letter names the
language the principle applies to, and the first digit names the level of
language the principle works at.
[MAINTAINING.md](MAINTAINING.md#ids) defines the letters and the levels,
and how to add, revise, and retire a principle.

## License

Licensed under either of

 * Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <http://www.apache.org/licenses/LICENSE-2.0>)
 * MIT license ([LICENSE-MIT](LICENSE-MIT) or <http://opensource.org/licenses/MIT>)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
