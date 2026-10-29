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
| [J101](plain-language/references/japanese.md#j101-母語話者で専門知識のある読み手を想定する) | 既定の読み手を、日本語を母語とし、分野の専門知識を持つ人とする。 |
| [J102](plain-language/references/japanese.md#j102-文体を文書の種類に合わせて統一する) | 文体は文書の種類を参考に選び、文書内で統一する。敬語は簡素にする。 |
| [J301](plain-language/references/japanese.md#j301-主題を保つ) | 段落の主題を各文で保ち、主題の語を別の語の従属要素にしない。 |
| [J302](plain-language/references/japanese.md#j302-因果と逆接を接続詞で示す) | 因果と逆接は接続詞で明示し、並列と添加は句点に任せる。 |
| [J303](plain-language/references/japanese.md#j303-箇条書きの形式をそろえる) | 箇条書きの各項目は、短い句か文のどちらかにそろえる。句には句点を付けず、文には付ける。 |
| [J401](plain-language/references/japanese.md#j401-接続助詞がを逆接と対比に使う) | 接続助詞「が」は逆接と対比に使い、前置きは接続詞や副詞句に置き換える。 |
| [J402](plain-language/references/japanese.md#j402-読点で係り受けを変えない) | 読点は係り受けを変えない範囲で打ち、係り受けを示す必要のない位置には打たない。 |
| [J501](plain-language/references/japanese.md#j501-用語を概念で統一する) | 同じ概念には同じ用語を使い、同じ語が異なる概念を指すときは区別する。 |
| [J502](plain-language/references/japanese.md#j502-英語由来の用語の表記を選ぶ) | 英語由来の専門用語とビジネス用語は、英単語を訳さず、概念の呼び名として定着した表記で書く。 |
| [J503](plain-language/references/japanese.md#j503-専門用語を積極的に使う) | 専門用語を積極的に使い、読み手にとって難しいと判断した語には補足を付ける。 |
| [J504](plain-language/references/japanese.md#j504-略語に展開形を併記する) | 略語には初出で展開形を併記する。 |
| [J505](plain-language/references/japanese.md#j505-固有名詞は定着した表記で書く) | 固有名詞は日本語で定着した表記で書き、人名は初出で綴りを添える。 |
| [J601](plain-language/references/japanese.md#j601-機能語をひらがなで書き常用漢字を基本にする) | 機能語はひらがなで書き、常用漢字表を基本にする。分野で定着した表外字の語は漢字で書く。 |
| [J602](plain-language/references/japanese.md#j602-漢字の誤変換が疑われる字を直す) | 漢字の誤変換が疑われる字は、辞書にある語形に直す。 |
| [J603](plain-language/references/japanese.md#j603-カタカナ語の長音を統一する) | カタカナ語の語尾の長音は原語の綴りで決め、文書内で統一する。 |
| [J604](plain-language/references/japanese.md#j604-半角と全角を使い分ける) | 数字と英字は半角で書き、半角文字の前後に半角スペースを置く。記号は係る文字に合わせる。 |

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
