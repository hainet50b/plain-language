---
name: plain-language-compare
license: MIT OR Apache-2.0
description: >-
  Run one prompt with and without the plain-language skill, across versions
  of it, or across models, and show the replies side by side. Use when the
  user asks to compare, try, or demonstrate what the plain-language skill does
  to a reply, how models differ under it, or to check a report: to reproduce
  the expression it describes, or to confirm that the expression no longer
  appears.
---

# plain-language-compare

This skill runs one prompt with and without the plain-language skill, across
versions of it, or across models, and shows the replies side by side, so
that a person can see what changes between them.

## Terms

| Term | Meaning |
| --- | --- |
| prompt | The instruction sent to the model, followed by the source text when the prompt edits or translates something. |
| principles | The principle files the model reads before it replies: none, the installed skill, a version in the repository, or any directory holding them. |
| sample | One reply to the prompt from one model under one set of principles. |
| comparison | One prompt, and the samples for it under each set of principles and each model, recorded in one directory. |

## Structure of a comparison

A comparison is one directory with these files:

```text
2026-09-13-strangler-fig/
├── comparison.json         principles, models, and for each sample its file, model, cost, and timing
├── index.html              the side-by-side view; opens offline
├── prompt/
│   ├── prompt.md           the instruction
│   └── source.md           the source text, when there is one
├── principles/
│   └── installed.md        the exact text given to the model as those principles
└── samples/
    ├── none.default/       one directory per set of principles and model
    │   ├── 1.md            one sample
    │   └── 2.md
    └── installed.default/
        ├── 1.md
        └── 2.md
```

Comparisons are written to the local data directory:

| System | Directory |
| --- | --- |
| Windows | `%LOCALAPPDATA%\plain-language\comparisons` |
| macOS | `~/Library/Application Support/plain-language/comparisons` |
| Linux | `$XDG_DATA_HOME/plain-language/comparisons`, or `~/.local/share/plain-language/comparisons` |

## Make a comparison

`scripts/compare.py` makes a comparison. The rest of this skill, under
`assets/`, is the page template and a bundled library that the script reads
on its own. The script needs:

- Python 3.12 or later, with no packages beyond the standard library.
- Claude Code, because the script calls the model through the `claude`
  command.

Run `python scripts/compare.py --help` first. It lists every option and how
to name a set of principles; this file does not repeat them.

### Typical runs

To see what the skill does to one prompt:

```sh
python scripts/compare.py "Explain the Strangler Fig pattern." \
  --name strangler-fig \
  --model sonnet \
  --open
```

To check a report:

```sh
python scripts/compare.py \
  --report-file path/to/2026-09-15-idempotent-gloss.md \
  --name idempotent-gloss \
  --model sonnet \
  --open
```

To compare the committed principles with the ones being edited, in a
checkout of the plain-language repository:

```sh
python scripts/compare.py \
  --report-file evals/reports/2026-09-15-idempotent-gloss.md \
  --name idempotent-gloss \
  --principles HEAD \
  --principles worktree \
  --model sonnet \
  --samples 2 \
  --repo .
```

To see how models differ under the same principles:

```sh
python scripts/compare.py "Explain the Strangler Fig pattern." \
  --name strangler-fig \
  --principles installed \
  --model sonnet \
  --model opus \
  --samples 2
```

### Before running

1. Run the command with `--dry-run` first. It prints the prompt, the
   principles, the agent and models, the number of model calls, and the
   output directory, and calls no model.
2. Show that output to the user and ask for permission to run. Say plainly
   when the run is large: many model calls, more than one model, or more
   than one sample per set of principles.
3. Run the command without `--dry-run` only after the user agrees.

### Rules

- Pass `--name` with a short English slug that names the topic, such as
  `strangler-fig`. It follows the date in the comparison's directory name,
  so that a person can pick the comparison out of a listing later. For a
  report, reuse the slug from the report's file name.
- Keep token use low. Leave `--samples` at 1 unless the user wants to see
  how much the replies vary. Unless the user names a model, propose the
  least capable model that can answer the prompt, such as `sonnet`, and
  pass it with `--model`; the agent's default is often its most capable and
  most expensive model. Use the default or a stronger model only when the
  user asks for it or when the comparison is about that model.

## Show the comparison

Pass `--open` so that the page opens in the browser as soon as the
comparison is written; the script also prints the directory. The page opens
one pane per set of principles and model, each showing one sample. A pane
can be switched to any sample of any set, so two samples of the same set
can be read next to each other.

The arrangement of the panes lives in the URL after `#`: one entry per pane
in the form `model,principles,sample`, entries separated by `;`, model and
principles URI-encoded. When you report a comparison, give the user the URL
for the arrangement they are likely to want, not only the directory.

The first sample without and with the installed principles:

```text
index.html#default,none,1;default,installed,1
```

Two samples of the same set, to see how much the replies vary:

```text
index.html#default,installed,1;default,installed,2
```

When the user asks to keep a comparison, move its directory into
`evals/comparisons/` in a checkout of the plain-language repository, and
drop the `-2` or `-3` suffix from its name as you do.
