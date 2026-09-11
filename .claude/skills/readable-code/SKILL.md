---
name: readable-code
description: >-
  Read this skill before writing, editing, or reviewing code in any language.
  It makes code readable to people who do not write that language every day
  and easy to audit: every operation and concept gets a name that states its
  intent, control flow stays shallow, idioms specific to the language give
  way to plain constructs, and comments are removed except where the code
  cannot say why.
---

# readable-code

Write code that a reader who does not write this language every day can
audit. The reader should recognize what each part does from its name, check
each part on its own, and never need to decode a construct.

These principles govern how code reads, not what it does or how fast it
runs. Apply them to new code, to edits, and to reviews. When they conflict
with a convention that an external contract or the ecosystem dictates, keep
the convention and say so.

## Principle index

| ID | Principle |
| --- | --- |
| [R01](#r01-write-for-a-reader-who-does-not-write-the-language-daily) | Prefer plain constructs to idioms that only fluent readers recognize. |
| [R02](#r02-name-every-operation-and-concept) | Give every operation and concept a name that states its intent. |
| [R03](#r03-use-one-name-per-concept) | Use one name for one concept, and different names for different concepts. |
| [R04](#r04-make-each-unit-checkable-on-its-own) | Make each function checkable from its signature and body alone. |
| [R05](#r05-keep-control-flow-shallow) | Leave the main path at the shallowest indentation and exit early on the rest. |
| [R06](#r06-remove-comments-that-code-can-replace) | Remove comments; keep only what the code cannot say. |
| [R07](#r07-show-what-a-pattern-matches) | Give every regular expression an example of what it matches. |

### R01 Write for a reader who does not write the language daily

**Application.** When a plain construct and a language-specific idiom
express the same thing, use the plain construct. Prefer a loop with a
clear body to a nested comprehension, an explicit condition to a truthiness
trick, a named function to a lambda passed inline, and an ordinary call to
metaprogramming, decorators that change behavior, operator overloading, or
reflection. Use an idiom only when the plain form would be much longer or
would hide the intent.

**Reason.** An idiom is a shortcut for readers who already know it. A
reader who meets it for the first time has to stop and decode it, and an
auditor who decodes it wrongly approves the wrong behavior.

**Example.** Prefer

```python
counts_by_level = {}
for principle in principles:
    level = principle.id[1]
    counts_by_level[level] = counts_by_level.get(level, 0) + 1
```

to

```python
counts_by_level = Counter(p.id[1] for p in principles)
```

when the reader may not know `Counter`.

[Back to the principle index](#principle-index)

### R02 Name every operation and concept

**Application.** Give a name to each operation the reader must recognize
and to each value the reader must track. Name operations with verb phrases
that state the intent, and values with noun phrases that state what they
hold. Do not abbreviate. Put a unit in the name when a number could be read
in more than one unit. Avoid names that fill space without narrowing the
meaning, such as `data`, `result`, `helper`, `process`, and `manager`.

A reader who sees only a function's name and the names it calls should be
able to say what the function does. The reader does not need to read the
code from top to bottom if every step is named.

**Reason.** Names are how a reader navigates. A name that states the intent
lets the reader decide whether to read the body at all, and lets the reader
check the body against a stated expectation.

**Example.** Prefer `timeout_seconds` to `timeout`, `retired_ids` to
`ids2`, and `load_index_rows(path)` to `process(path)`.

[Back to the principle index](#principle-index)

### R03 Use one name per concept

**Application.** Use the same word for the same concept throughout the
code, including the words the surrounding documents use. Use different
words for different concepts. Do not vary a name to avoid repetition, and
do not reuse a name for a different thing in a different scope.

**Reason.** A second word for the same thing makes the reader look for a
difference that does not exist. One word for two things hides a difference
that does.

**Example.** If the documents call a unit of evaluation a "case", the code
uses `case`, `case_dir`, and `load_case`, not `test`, `example`, or `spec`.

[Back to the principle index](#principle-index)

### R04 Make each unit checkable on its own

**Application.** Give each function explicit inputs and outputs. Do not
read or write state that the signature does not show. Declare the types of
parameters and return values where the language allows. Keep a function to
one operation, so that its name can be checked against its body.

**Reason.** An auditor checks one unit at a time. A unit that depends on
hidden state cannot be checked without reading the rest of the program.

**Example.** Prefer

```python
def render_row(principle: Principle, anchor: str) -> str:
```

to a function that reads `principle` from a module-level variable and
writes the row to a global list.

[Back to the principle index](#principle-index)

### R05 Keep control flow shallow

**Application.** Handle invalid or exceptional cases first and leave them
with an early return or `continue`. Keep the main path at the shallowest
indentation. Treat three levels of nesting as the ceiling; past that, name
the inner block as a function under [R02](#r02-name-every-operation-and-concept).

**Reason.** Each level of nesting is a condition the reader must hold in
mind while reading the lines below it. The main path is what the reader
most needs to check, and it should not sit under the largest pile of
conditions.

**Example.** Prefer

```python
for row in rows:
    if row.retired:
        continue
    if row.id not in headings:
        report_missing(row.id)
        continue
    check_anchor(row)
```

to the same logic nested inside `if not row.retired:` and
`if row.id in headings:`.

[Back to the principle index](#principle-index)

### R06 Remove comments that code can replace

**Application.** Do not write comments that say what the code does; the
names say it. Delete docstrings that repeat the signature, banners that
divide a file into sections, and code that has been commented out. Keep a
comment only for a fact the code cannot express: a constraint imposed by an
external system, a consequence that is not visible at the call site, or
the reason a plain alternative was rejected. Keep such a comment to one or
two lines.

**Reason.** A comment that restates the code is one more thing to read and
one more thing that goes stale. A stale comment is trusted and wrong. If a
block needs a comment to be understood, the block needs a name.

**Example.** Delete `# loop over the rows`. Keep
`# The grader model truncates input past 100 KB; split before sending.`

[Back to the principle index](#principle-index)

### R07 Show what a pattern matches

**Application.** Next to every regular expression, add one line that shows
a string it matches, and, when the pattern has alternatives or exclusions,
one that it does not. Name the pattern after what it recognizes.

**Reason.** A regular expression is the one construct that even fluent
readers decode slowly. An example lets the reader verify the pattern by
comparison instead of by simulation.

**Example.**

```python
# matches "| [P302](#p302-order-information-by-purpose) | Lead with ... |"
INDEX_ROW = re.compile(r"^\| \[([PJE]\d{3})\]\((#[^)]+)\) \| (.+?) \|$")
```

[Back to the principle index](#principle-index)

## Reviewing

When reviewing code, point at the line, name the principle by ID, and show
the readable form. Report readability findings separately from findings
about behavior.
