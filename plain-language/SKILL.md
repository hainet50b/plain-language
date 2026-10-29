---
name: plain-language
license: MIT OR Apache-2.0
description: >-
  Read this skill before you write text a person will read, such as an
  explanation, a report of progress or results, or a document, and before
  you edit, review, or translate text. Read it even when the request does
  not mention wording. It helps the text say plainly what matters most to
  its reader at that moment, in the terms that reader uses, without the
  hedges, asides, and other additions that bury the point. When you edit,
  it keeps any meaning you were not asked to change. A one-line fact or
  casual conversation does not call for it.
---

# plain-language

Apply these principles so readers can follow the text and assess its
meaning.

When writing, editing, or reviewing text in a language that has a language
reference below, or translating into that language, also read that
reference. The source language of a translation alone does not call for
its reference.

| Language | Reference |
| --- | --- |
| English | [references/english.md](references/english.md) |
| Japanese | [references/japanese.md](references/japanese.md) |

When principles conflict, follow
[P102](#p102-resolve-conflicts-by-precedence).

## Principle index

Each principle has application guidance, a reason, and an example.

| ID | Principle |
| --- | --- |
| [P101](#p101-say-the-point-itself) | Say the point itself, not the circumstances around it. |
| [P102](#p102-resolve-conflicts-by-precedence) | Apply meaning and logical structure first, consistent terms second, and this file's principles before a language reference. |
| [P201](#p201-support-the-point-as-far-as-the-reader-needs) | Give the reasons and background the reader needs, and no more. |
| [P301](#p301-make-references-clear) | Use pronouns when their references are clear in context. |
| [P401](#p401-express-actions-with-verbs) | Express actions with verbs and avoid unnecessary nominalization. |
| [P402](#p402-say-it-in-a-sentence) | Say how the parts relate in words, not with a label or a colon. |
| [P501](#p501-keep-terms-consistent) | Use the same term for the same concept. |
| [P502](#p502-use-the-terms-readers-in-the-field-use) | Use the terms readers in the field use, written their way. |
| [P701](#p701-keep-the-meaning-you-were-not-asked-to-change) | Keep the meaning you were not asked to change. |

## 1xx Frame

### P101 Say the point itself

Decide what you mean to tell the reader, and write it in words that name
it directly. Do not describe the point through the circumstances around
it. The reader takes what a sentence says as its point, so a sentence about
the circumstances delivers a different point from the one you meant.

[Back to the principle index](#principle-index)

### P102 Resolve conflicts by precedence

**Application.** When principles conflict, apply them in this order:

1. Preserve meaning and logical structure ([P701](#p701-keep-the-meaning-you-were-not-asked-to-change)).
2. Keep terms consistent ([P501](#p501-keep-terms-consistent)).
3. Apply the remaining principles.

The principles in this file take precedence over the principles in a
language reference. When this order does not settle a conflict, judge by
[P701](#p701-keep-the-meaning-you-were-not-asked-to-change) and
[P101](#p101-say-the-point-itself).

**Reason.** Without a fixed order, the same conflict is settled differently
from one passage to the next, and the text becomes inconsistent.

**Example.** Replacing a repeated term with a synonym would improve the
rhythm of a sentence but break P501. Keep the term.

[Back to the principle index](#principle-index)

## 2xx Content

### P201 Support the point as far as the reader needs

Give the reason that lets the reader trust the point or act on it. Add
background only when the reader needs it to follow that reason or asked
why. Say that one thing caused another only when you have checked it;
otherwise say what you observed.

[Back to the principle index](#principle-index)

## 3xx Discourse

### P301 Make references clear

**Application.** Use a pronoun when its reference is clear in context.
Otherwise repeat the noun, even next to another occurrence. Consider the
distance from the noun and the plausible interpretations. A continuing
topic often allows a pronoun; a change in actor or topic may require a noun.

**Reason.** A pronoun can reduce repetition without changing the term.
Its usefulness depends on whether readers can identify the reference.

**Example.** The pronoun has a clear reference here:

> The client sends a request. The server validates it.

The actor is unclear here:

> The client sends a request to the server. It validates the request.

If the server is the actor, replace "It" with "The server."

[Back to the principle index](#principle-index)

## 4xx Sentence

### P401 Express actions with verbs

**Application.** Express actions directly with verbs where possible.
Avoid unnecessary nominalization: expressing an action as a noun when a
verb would serve the meaning. Keep noun forms when needed, and preserve
the topic and logical structure.

**Reason.** A noun combined with a general verb can add words without
adding meaning.

**Example.** Prefer "The server validates the request" to "The server
performs validation of the request." Keep "The server cancels validation":
cancellation is the action, and validation is its object.

[Back to the principle index](#principle-index)

### P402 Say it in a sentence

Write what you mean in sentences whose words say how the parts relate. Do
not open a sentence or a list item with a word that only names what
follows, and do not join two parts with a colon. Say the relation in words
instead.

[Back to the principle index](#principle-index)

## 5xx Lexicon

### P501 Keep terms consistent

Use the same term for the same concept throughout the text, and different
terms for different concepts. A new word makes the reader check whether
the concept changed, so do not switch to a synonym to avoid repetition. A
pronoun ([P301](#p301-make-references-clear)) or another form of the same
word ([P401](#p401-express-actions-with-verbs)) keeps the concept.

[Back to the principle index](#principle-index)

### P502 Use the terms readers in the field use

Name a concept by the term readers in the field use in their documents,
code, and conversation, written the way they write it. Write product and
project names exactly as their owners do. Do not replace an established
term with a general phrase or a literal translation. When a request or a
source describes a concept instead of naming it, name the concept; the
description is not a term [P501](#p501-keep-terms-consistent) asks you to
keep. Explain a term only when the reader needs it.

[Back to the principle index](#principle-index)

## 7xx Change

### P701 Keep the meaning you were not asked to change

When you edit or translate, keep what the text claims, including which
point is the main one, its conditions, how certain it is, how strong its
requirements are, and its causes. Change only the wording and
presentation. In a translation, add nothing the source does not say.

[Back to the principle index](#principle-index)

## Foundations

These principles are drawn from the sources below and adjusted by the
editorial preferences stated here. They do not claim compliance with a
formal plain-language standard. Routine use does not require browsing the
sources.

- [Principles of plain language](https://digital.gov/guides/plain-language): adapt content, information order, and presentation to the reader's knowledge and purpose.
- [Gopen and Swan, The Science of Scientific Writing](https://courses.ems.psu.edu/styleforstudents/print/c10_p6.html): use reader expectations, topic continuity, emphasis, and grammatical structure to guide edits.
