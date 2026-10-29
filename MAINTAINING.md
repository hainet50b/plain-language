# Maintain the principles

This file is for the people who maintain the plain-language skill. The
agent that applies the principles does not read it, so it stays outside
the skill directory.

## IDs

An ID is a letter and three digits, such as `P501`. The letter names the
language the principle applies to, and the first digit names the level: the
smallest span of text a reader needs to tell whether the principle is
followed.

| Letter | Applies to |
| --- | --- |
| P | Every language |
| E | English text |
| J | Japanese text |

| IDs | Level | Span |
| --- | --- | --- |
| 1xx | Frame | The whole text and the relationship among writer, reader, and editor |
| 2xx | Content | The information the text includes |
| 3xx | Discourse | Several sentences |
| 4xx | Sentence | One sentence |
| 5xx | Lexicon | One word or phrase |
| 6xx | Orthography | Characters and symbols |
| 7xx | Change | The text before and after an edit, or a source and its translation |

A principle that requires consistency, such as P501, is judged across the
whole text, wider than the span of its level. Classify such a principle by
the unit it keeps consistent instead: a term belongs to 5xx, a spelling to
6xx.

An ID names the principle's scope: what the principle is about. Revising
how the principle handles that scope keeps the ID, even when the heading
changes. Changing the scope retires the ID and assigns a new one. Give a
new principle the number after the highest one assigned so far within its
level, so that a retired number stays taken, and never renumber an existing
principle; gaps are expected. Update a principle's row in the index in
[README.md](README.md#principles) together with its section.

## Retired IDs

Record a retired ID of any letter in the table below. Successor names the
principle that took over the scope at retirement, or `—` when none did.
Note states the reason in one sentence. Never reuse a retired ID, and do
not revise the table later: a principle added afterwards is a new
principle, whatever its resemblance to a retired one.

| Retired ID | Successor | Note |
| --- | --- | --- |
| P102 | — | Few principles remain, so the model settles conflicts. |
| P103 | — | Voice needed protecting only from rules that are now gone. |
| P202 | — | The skill no longer prescribes how to choose examples. |
| P301 | — | The model already uses pronouns well, and its rule to repeat nouns added repetition. |
| P302 | — | The skill no longer prescribes where the point goes. |
| P303 | P701 | P701 covers unsupported causes in an edit; P201 covers them in new text. |
| P304 | P402 | Only the rule against labels and colons remained, and it is about one sentence. |
| P401 | P101 | Nouns for actions are common and clear; P101 covers those that hide the point. |
| P702 | P701 | Merged into one principle about edits and translations. |
| E101 | E501 | The model judges the reader's English on its own; E501 keeps the word choice. |
| E301 | — | The model chooses active or passive voice well without a rule. |
| E302 | — | The model places emphasis well without a rule. |
| E401 | — | It asked for a "that" the reader does not need, against native usage and E303. |
| E402 | — | It allowed both keeping and moving an interruption, so it gave no direction. |
