---
name: plain-language-report
license: MIT OR Apache-2.0
description: >-
  Record an expression in a reply that feels unnatural to a reader as a
  report, with the prompt that produces it, so that the maintainers can fix
  the plain-language skill. Use when the user points at an unnatural
  expression in a reply, says how replies should be worded, or asks to
  list, show, or import reports.
---

# plain-language-report

This skill records an expression that feels unnatural to a reader as a
report: the expression, the reader's impression of it, and a prompt that
produces it. The agent asks what felt unnatural and builds the report from
the answer.

## Terms

| Term | Meaning |
| --- | --- |
| reporter | The person who found the unnatural expression and reported it. |
| report | One file that records the expression, the reporter's impression of it, and a prompt that produces it. |

## Structure of a report

A report is one Markdown file with frontmatter and sections:

```markdown
---
status: open
principles: []
---

## Prompt

Explain to a backend developer why a payment API should make its charge
endpoint idempotent.

## Problem

### Expression

The endpoint should be safe to repeat, meaning that calling it twice does
the same thing as calling it once.

### Impression

The reader is a backend developer. "Safe to repeat" reads like the agent
avoided the word I used in the question.

## Expected

The endpoint should be idempotent: calling it twice has the same effect as
calling it once.

## Comparisons
```

The frontmatter records what became of the report:

| Field | Content |
| --- | --- |
| `status` | `open` when the report is written; the maintainers change it to `resolved` or `not-planned`. |
| `principles` | Empty when the report is written. The maintainers later add the IDs of the principles related to the expression, such as `P502`. |

The sections record the report itself:

| Section | Content |
| --- | --- |
| `## Prompt` | The instruction sent to the model. |
| `## Source` | The text the prompt edits or translates. Present only when there is one. |
| `## Problem` | Two subsections. `### Expression` names the expression: a word, a description such as "every reply ends with an offer", a span quoted from a reply, or several of these. `### Impression` gives what the reporter felt about it. |
| `## Expected` | How the expression should read. |
| `## Comparisons` | Empty when the report is written. The maintainers later add the comparisons they make from the report. |

## Make a report

Making a report is a conversation: hear what felt unnatural, build the
report from it, show the report, and go back when it misses the point.

### Hear the impression

Let the reporter say what felt unnatural in the reply, in whatever order
and detail they have. Do not put them through a fixed set of questions.
Help them say what they have not yet put into words:

- Restate what they said in your own words and ask whether that is what
  they mean.
- When the expression is not yet concrete, draft an example that shows it
  and ask whether it matches. When a reply in the current conversation
  seems to be what they mean, you may offer spans from it. When the
  reporter does not identify the expression, continue with your general
  understanding of it.
- Ask how they would write it. The answer shows what they want.

Move on to building the report when you have these three things:

1. The expression: a word, a description such as "every reply ends with an
   offer", a span from a reply, or several of these.
2. What the reporter felt was unnatural about it.
3. Enough to write a prompt that produces the expression.

### Build the report

Turn what you heard into the form of a report without further work from
the reporter.

- Under `## Prompt`, write a prompt that produces the expression. When the
  reporter gave the prompt, use theirs. Put the text the prompt edits or
  translates under `## Source`; when that text is long, keep only the part
  needed to produce the expression.
- Under `### Expression`, put the expression in the forms you heard it: a
  word, a description, a quotation, or several of these.
- Under `### Impression`, put what the reporter said. You may soften the
  wording so that the reporter is comfortable handing the report on, but
  keep what they felt.
- Under `## Expected`, write how the expression should read, in general
  terms. Take in what the reporter said when they said how they would
  write it.
- Replace names of people, customers, and internal systems, and details of
  the work, with equivalents that still produce the expression. Replace
  uncommon concepts with common ones. Do neither where it would change
  what the reporter means.

Write what the reporter said, and what you write as description, in the
reporter's language. Write what the model reads and what it should write,
that is `## Prompt`, `## Source`, a quotation under `### Expression`, and
the text under `## Expected`, in the language of the reply the report is
about.

### Show and write

Show the report as the whole file inside a fenced code block, the same way
as when the user asks to see a report. Say what you replaced. Ask whether
the report is right and whether it captures what the reporter felt. When
it does not, go back to hearing the impression; the exchange is how the
reporter finds out what they want. When the reporter agrees, write the
file to `~/.plain-language/reports/<YYYY-MM-DD>-<slug>.md`, with a short
English slug for the topic such as `idempotent-gloss`, and print the path.

## List and show reports

When the user asks what reports there are, list the files in
`~/.plain-language/reports/` as a table with one row per report: the date,
the slug linked to the file, and the `status`.

When the user asks about one report, print the whole file inside a fenced
code block, so that they can copy it with one click and paste it to a
maintainer.

## Import a report

The maintainers keep reports in `evals/reports/` in a checkout of the
plain-language repository, where anyone can read them. Importing a report
copies it there. Recording what became of it comes later, when the
maintainers have checked it.

### Copy the report

When the user asks to import a report, first read it for anything that
should not be published: names, internal details, and source text that is
not the reporter's to share. Propose replacements that keep the expression
and what the reporter felt, and apply them after the user agrees. Then
copy the file into `evals/reports/` without changing its name.

### Record the outcome

When the maintainers have checked the report, for example by reproducing
the expression with the plain-language-compare skill, and the user says
what became of it, change `status` to `resolved` or `not-planned` and add
to `principles` the IDs of the principles related to the expression.
Under `## Comparisons`, add one bullet for each comparison kept in
`evals/comparisons/` for the report: a link to the comparison and a
summary of what it showed.
