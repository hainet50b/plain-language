![plain-language](assets/banner.png)

![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)

An agent skill that helps an AI coding agent say its point itself, in
the reader's terms. It applies to the explanations, reports, and
documents the agent writes, and to any text it edits, reviews, or
translates. A skill is a directory of instructions an agent loads on
demand, following the
[Agent Skills specification](https://agentskills.io/specification).

Current models write sentences that are correct one by one, yet the reader
often takes away a different point from the one meant. The text talks about
the circumstances around the point instead of the point, uses terms from
outside the reader's field, or, in an edit, changes meaning nobody asked to
change. The skill targets these three habits.

This repository also holds the tools that maintain the skill. One runs a
prompt with and without the skill and shows the replies side by side.
Another records an expression that felt unnatural to a reader as a report,
with the prompt that produces it, so that the maintainers can fix the
principles.

## Contents

| Path | Description |
| --- | --- |
| [plain-language/SKILL.md](plain-language/SKILL.md) | The shared principles, each with an ID. |
| [plain-language/references/english.md](plain-language/references/english.md) | Principles for English text that the agent produces or reviews. |
| [plain-language/references/japanese.md](plain-language/references/japanese.md) | Principles for Japanese text that the agent produces or reviews. |
| [plain-language-compare/](plain-language-compare/SKILL.md) | Skill that runs one prompt with and without the plain-language skill, across versions of it, or across models, and shows the replies side by side. |
| [plain-language-report/](plain-language-report/SKILL.md) | Skill that records an expression that feels unnatural to a reader as a report, with the prompt that produces it, by asking the reader what felt unnatural. |
| [evals/](evals/README.md) | The reports and comparisons worth keeping. They serve as the regression suite and as evidence of what the skill does. |
| [MAINTAINING.md](MAINTAINING.md) | How principle IDs are assigned, and the record of retired IDs. The agent does not read it. |
| [scripts/validate.py](scripts/validate.py) | Checks the principle files and the index in this README against each other, along with IDs, levels, links, and the retired table. |

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

## Principles

<details>
<summary>Shared principles</summary>

| ID | Principle |
| --- | --- |
| [P101](plain-language/SKILL.md#p101-say-the-point-itself) | Say the point itself, not the circumstances around it. |
| [P201](plain-language/SKILL.md#p201-support-the-point-as-far-as-the-reader-needs) | Give the reasons and background the reader needs; state a cause only when you have checked it. |
| [P402](plain-language/SKILL.md#p402-say-it-in-a-sentence) | Say how the parts relate in words, not with a label or a colon. |
| [P501](plain-language/SKILL.md#p501-keep-terms-consistent) | Use the same term for the same concept. |
| [P502](plain-language/SKILL.md#p502-use-the-terms-readers-in-the-field-use) | Use the terms readers in the field use, written their way. |
| [P701](plain-language/SKILL.md#p701-keep-the-meaning-you-were-not-asked-to-change) | Keep the meaning you were not asked to change. |

</details>

<details>
<summary>English principles</summary>

| ID | Principle |
| --- | --- |
| [E303](plain-language/references/english.md#e303-let-context-carry-what-the-reader-already-knows) | Use the bare noun when the context already identifies it. |
| [E501](plain-language/references/english.md#e501-use-everyday-words) | Use the word a native speaker would use with a colleague. |
| [E502](plain-language/references/english.md#e502-say-what-an-idiom-means) | Write the plain meaning instead of an idiom whose words do not give it. |

</details>

<details>
<summary>Japanese principles</summary>

| ID | Principle |
| --- | --- |
| [J402](plain-language/references/japanese.md#j402-読点で係り受けを変えない) | 読点は係り受けを変えない範囲で打ち、係り受けを示す必要のない位置には打たない。 |
| [J502](plain-language/references/japanese.md#j502-英語由来の用語の表記を選ぶ) | 英語由来の専門用語とビジネス用語は、英単語を訳さず、概念の呼び名として定着した表記で書く。 |
| [J605](plain-language/references/japanese.md#j605-技術文書で半角と全角を使い分ける) | 技術的な文章では、数字と英字を半角で書き、前後に半角スペースを置く。 |

</details>

## License

Licensed under either of

 * Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or <http://www.apache.org/licenses/LICENSE-2.0>)
 * MIT license ([LICENSE-MIT](LICENSE-MIT) or <http://opensource.org/licenses/MIT>)

at your option.

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.
