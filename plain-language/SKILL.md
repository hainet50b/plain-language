---
name: plain-language
license: MIT OR Apache-2.0
description: >-
  Read this skill before you write any reply of your own in a chat, except
  a one-line statement of a fact or result, and before composing, writing,
  editing, reviewing, or translating any prose. It applies plain-language
  principles to keep terminology consistent, make logical structure clear,
  and use wording suited to the reader, even when the request does not
  mention wording.
---

# plain-language

Apply these principles so readers can follow the text and assess its
meaning. Adapt them to the reader and purpose, regardless of anyone's
native language.

When writing, editing, translating into, or reviewing English, also read
[references/english.md](references/english.md). Read that reference for
English output or review, not merely because a source is in English.

Preserve meaning and logical structure before improving style. Among
stylistic preferences, consistent terminology has the highest priority.

## Principle index

Each principle has application guidance, a reason, and an example.

| ID | Principle |
| --- | --- |
| [P01](#p01-preserve-meaning) | Preserve meaning and logical structure when improving style. |
| [P02](#p02-keep-terms-consistent) | Use the same term for the same concept. |
| [P03](#p03-make-references-clear) | Use pronouns when their references are clear in context. |
| [P04](#p04-adapt-to-the-reader-and-task) | Match the explanation and amount of detail to the reader and task. |
| [P05](#p05-order-information-by-purpose) | Lead with conclusions for instructions and proposals; lead with premises to develop understanding. |
| [P06](#p06-connect-information) | Connect new information to established context and make logical links clear. |
| [P07](#p07-give-reasons-and-select-background) | Normally give reasons; explain those reasons further when needed. |
| [P08](#p08-match-form-to-logical-structure) | Choose sentences, paragraphs, lists, and tables to show logical relationships. |
| [P09](#p09-express-actions-with-verbs) | Express actions with verbs and avoid unnecessary nominalization. |
| [P10](#p10-respect-technical-meaning) | Keep established technical terms and simplify the surrounding language first. |
| [P11](#p11-choose-minimal-representative-examples) | Keep examples relevant, minimal, and representative for the reader. |
| [P12](#p12-preserve-useful-voice) | Preserve voice and figurative language that serve the passage. |
| [P13](#p13-edit-and-translate-transparently) | Improve presentation, explain changes in emphasis, and confirm changes in meaning. |

## Shared principles

### P01 Preserve meaning

**Application.** Preserve the intended meaning and logical structure,
including:

- The relationship between main points and supporting details.
- The scope of conditions and exceptions.
- Quantities and uncertainty.
- The strength of claims and requirements.

Give these relationships and distinctions priority over brevity and
grammatical preferences. Use [P13](#p13-edit-and-translate-transparently)
to decide when a deliberate change needs explanation or confirmation.

**Reason.** An edit can retain the same facts while changing what a claim
means or how much weight a supporting detail receives.

**Example.** Keep "may fail" when failure is uncertain. Changing it to
"will fail" makes the claim stronger.

### P02 Keep terms consistent

**Application.** Use the same term for the same concept throughout the
text, including objects and actions. Keep different concepts distinct.
Respect established technical terms and exact product or project names.
Do not introduce synonyms merely to avoid repetition.

Use pronouns under [P03](#p03-make-references-clear) and related noun and
verb forms under [P09](#p09-express-actions-with-verbs) when they preserve
the same concept.

**Reason.** A different term can suggest a different concept, making
readers check whether the meaning has changed.

**Example.** If "request" and "message" name the same object, use "request"
in both sentences:

> The client sends a request. The server validates the request.

### P03 Make references clear

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

### P04 Adapt to the reader and task

**Application.** Consider what the reader knows and what the text should
help them do or understand. Assess language proficiency separately from
subject knowledge. Provide the amount of detail that the task needs.
Short answers, questions, and progress updates do not need extra sections
or tables.

When translating, follow [P13](#p13-edit-and-translate-transparently);
do not add explanations that are absent from the source.

**Reason.** Familiarity with a language, product, or local convention does
not determine subject knowledge. Extra explanation can help one reader
while distracting another.

**Example.** For readers who know distributed systems but are less
familiar with English, keep "idempotent" and simplify the surrounding
sentences. Do not assume that they need a basic lesson in distributed systems.

### P05 Order information by purpose

**Application.** Choose the order for each passage according to its purpose.

| Purpose | Order |
| --- | --- |
| Give instructions or make a proposal | State the conclusion or requested action with essential conditions, then give reasons. |
| Develop understanding | Establish the necessary premises, explain their relationships, then reach the conclusion. |

README files often use the first order; essays often use the second.
Choose by the passage's purpose rather than fixing the order by document type.

**Reason.** Instructions help readers decide what to do. Explanations help
readers understand how a conclusion follows from its premises.

**Example.** A setup instruction can begin with "Restart the service to
apply the change," followed by the reason. An explanation of the same
setting can first describe when the service reads it, then explain why a
restart is required.

### P06 Connect information

**Application.** Use established context to introduce new information.
Keep the topic easy to follow and make necessary logical relationships
explicit. Place emphasis where it supports the intended point. State a
causal relationship only when the available information supports it.

**Reason.** Readers need to understand how each new point relates to the
preceding discussion. Adding an unsupported connection changes the meaning.

**Example.** These statements alone do not establish a cause:

> The file is missing. Processing stopped.

Use "Processing stopped because the file is missing" only when the missing
file is the established cause.

### P07 Give reasons and select background

**Application.** Normally explain the reasons for recommendations,
evaluations, choices, and interpretations. In documents, normally support
claims and decisions with reasons.

- Omit reasons when they are already shared or serve no useful role, as
  in an acknowledgment or a factual list.
- Add background when readers need it to understand a reason or when the
  task calls for deeper understanding.
- Keep enough explanation to avoid a logical gap.
- Use available evidence; do not invent a reason.
- For translation, preserve the source under
  [P13](#p13-edit-and-translate-transparently).

Distinguish these roles according to the question:

| Role | Function |
| --- | --- |
| Answer | Respond to the question. |
| Reason | Explain why the answer holds. |
| Background | Explain why the reason holds. |

These roles do not prescribe the order of the response. Use
[P05](#p05-order-information-by-purpose) to choose that order.

**Reason.** Reasons let readers assess an answer. Background can deepen
understanding, but readers do not always need it.

**Example.** A restart requirement is the answer. Reading the setting only
at startup is the reason. The design decision behind that behavior is
background. If the question asks why that design was chosen, the design
decision becomes part of the answer and its reason.

### P08 Match form to logical structure

**Application.** Choose the form that makes the relationships easy to follow.

| Relationship | Form |
| --- | --- |
| One condition with a few closely related actions | One sentence, if readers can follow it easily. |
| Short details about one of those actions | A separate sentence that clearly identifies the action or its result. |
| Many actions, branches, or complex nesting | A list that shows the relevant groups and levels. |
| Steps in a sequence | A numbered list. |
| Items compared on the same dimensions | A table. |
| Ideas developed through an explanation | Connected paragraphs. |

Keep parallel items parallel in wording and level of detail. Avoid fixed
word counts and item thresholds. Use two sentences when they show the
structure more simply than a list.

**Reason.** Sentence boundaries and visual groups show which conditions,
actions, and details belong together.

**Example.**

> If validation fails, the system keeps the existing settings and displays
> an error. The error includes the field name and explains why validation
> failed.

The first sentence groups two actions under one condition. The second
adds two details about the error.

### P09 Express actions with verbs

**Application.** Express actions directly with verbs where possible.
Avoid unnecessary nominalization: expressing an action as a noun when a
verb would serve the meaning. Keep noun forms when needed, and preserve
the topic and logical structure.

**Reason.** A noun combined with a general verb can add words without
adding meaning.

**Example.** Prefer "The server validates the request" to "The server
performs validation of the request." Keep "The server cancels validation":
cancellation is the action, and validation is its object.

### P10 Respect technical meaning

**Application.** Use established terms for technical concepts and preserve
their specific meanings. Improve readability first by simplifying the
surrounding wording and sentence structure. Do not replace a technical term
with a general expression merely because the reader's subject knowledge is
unknown. When translating, use established terms in the target language
where available.

Add a definition, explanation, or example when the reader's knowledge and
the passage's purpose call for it. When translating, follow
[P13](#p13-edit-and-translate-transparently); do not add explanations that
are absent from the source.

**Reason.** An easier word may broaden a technical meaning or erase a
necessary distinction. Established terms also let readers recognize a
concept and connect it to their subject knowledge.

**Example.** Keep "idempotent" rather than replacing it with "safe to repeat."
If readers need an explanation, write:

> This operation is idempotent: repeating it has the same effect as
> performing it once.

### P11 Choose minimal representative examples

**Application.** When choosing examples, especially for parentheses:

- Keep each example relevant to the passage's context.
- Use only as many examples as the explanation needs.
- Choose representative examples that most intended readers recognize.

Prefer examples that do not require knowledge of an unusual product or
case. Use one example when it is enough, and more when a distinction
requires them. Move substantial explanations out of parentheses.

**Reason.** An example should clarify the point without requiring readers
to learn unrelated details.

**Example.** In developer documentation, "structured data (such as JSON)"
can supply one familiar example. A different audience may need an
explanation of JSON.

### P12 Preserve useful voice

**Application.** Preserve perspective, rhythm, metaphor, and the development
of an experience when they serve an essay's purpose. Use figurative language
that readers can understand from the passage's context.

**Reason.** An essay can communicate through personal voice and the
development of an idea as well as through facts.

**Example.**

> The configuration file had become an outdated map: it still listed
> features that no longer existed.

The explanation makes the metaphor understandable within the passage.

### P13 Edit and translate transparently

**Application.** Actively improve wording, word order, sentence boundaries,
and presentation. Translation may split or join sentences and turn clearly
parallel items into lists. Preserve source information; do not add facts,
reasons, or explanations to make the translation more helpful.

Handle changes according to what they affect:

| Change | Action |
| --- | --- |
| Improve presentation while preserving intent, emphasis, and logical relationships | Make the change without a separate approval step. |
| Preserve meaning but change emphasis or how the argument is presented | Make the change, then briefly explain what changed and why. |
| Resolve a material ambiguity or change a claim, condition, requirement strength, or causal relationship | Ask first unless the user has already explicitly authorized the change. |

Keep editorial explanations separate from the edited or translated text.
Do not silently select an ambiguous actor or condition. Treat the promotion
of a supporting detail into a main claim as a change in emphasis, even
when the facts remain unchanged.

**Reason.** Editing can improve presentation while also changing how readers
interpret the text. Authors need visibility into those changes.

**Example.** Moving a conclusion to the beginning can be explained after
the edit. Changing "Save after validation" to "Save only if validation
succeeds" adds a condition and requires confirmation of the intended meaning.

## Maintain the principles

Keep each ID stable. Update an index entry and its linked section together.
Use an unused ID for a new principle.

## Foundations

These principles combine guidance from the sources below with the editorial
preferences stated here. They do not claim compliance with a formal
plain-language standard. Routine use does not require browsing the sources.

- [Principles of plain language](https://digital.gov/guides/plain-language): adapt content, information order, and presentation to the reader's knowledge and purpose.
- [Gopen and Swan, The Science of Scientific Writing](https://courses.ems.psu.edu/styleforstudents/print/c10_p6.html): use reader expectations, topic continuity, emphasis, and grammatical structure to guide edits.
