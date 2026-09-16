# evals

This directory holds the reports and comparisons worth keeping. Together
they serve as the regression suite for the plain-language skill and as
evidence of what the skill does. The repository is written in English, but
a report and the samples in a comparison are written in the language of
the reply that the report describes.

## Reports

A report records an expression in a reply that felt unnatural to a reader,
the reader's impression of it, and a prompt that produces it. Reports are
written with the [plain-language-report](../plain-language-report/SKILL.md)
skill. Each report carries its current status and the principles related
to the expression.

## Comparisons

A comparison shows how one prompt is answered under each set of principles
and by each model. Comparisons are made with the
[plain-language-compare](../plain-language-compare/SKILL.md) skill. Each
directory holds the prompt, one file per sample, `comparison.json` with the
models and the principles that produced the samples, and `index.html` with
the side-by-side view.

GitHub does not render `index.html`. To read a comparison side by side,
clone the repository and open the file in a browser; it works offline. The
part of the URL after `#` selects the samples that the panes show, one
entry per pane in the form `model,principles,sample`:

```text
index.html#claude-fable-5-1,HEAD,1;claude-fable-5-1,worktree,1
```

A link from a report is built this way, so that it opens the arrangement
that shows the expression the report describes.

## Past findings

| Report | Comparison | Language | Status | Principles |
| --- | --- | --- | --- | --- |
| [2026-09-15-loanword-kanji-reply](reports/2026-09-15-loanword-kanji-reply.md) | [2026-09-16-loanword-kanji-reply](comparisons/2026-09-16-loanword-kanji-reply/) | Japanese | resolved | [P502](../plain-language/SKILL.md#p502-respect-technical-meaning), [J502](../plain-language/references/japanese.md#j502-英語由来の用語の表記を選ぶ) |
