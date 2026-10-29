# English principles

Apply these additions when writing, editing, reviewing, or translating into
English. Use the [shared principles](../SKILL.md)
throughout.

## 1xx Frame

### E101 Write for readers without assuming advanced English

**Application.** By default, write for readers who may lack advanced
English usage or shared cultural knowledge. Assess language proficiency
separately from subject knowledge; do not simplify the subject matter.

**Reason.** English output often reaches readers who use English as a
second language. Advanced usage and cultural references cost them attention
that the content needs.

**Example.** Keep "idempotent" for readers who know distributed systems,
and write "use" rather than "utilize" around it.

## 3xx Discourse

### E301 Prefer topic continuity over active voice

**Application.** Choose active or passive voice to keep the topic easy to
follow. Prefer active voice when it serves that topic. When the action's
object is the topic, use passive voice if it preserves topic continuity.
Include the actor when the actor matters.

**Reason.** Making the actor the subject can shift attention away from
the object that the paragraph explains.

**Example.** In a paragraph about a report:

> The report contains personal information. The report is reviewed by the
> administrator before publication.

The report remains the topic, and the second sentence still identifies
the actor.

### E302 Place emphasis at syntactic closure

**Application.** Use familiar information at the start to connect with the
preceding text. Place important new information at syntactic closure when
that position gives it the intended emphasis. Syntactic closure is the
point where a clause or sentence becomes complete.

The stress position can contain a phrase or a longer unit, not just the
last word. Use it for the new information that deserves emphasis, rather
than for every new detail.

**Reason.** Gopen and Swan describe the stress position as a point of
syntactic closure where readers tend to give information emphasis.

**Example.**

> Before you enable automatic retries, check whether the operation is
> idempotent.

The task provides context, and the property to check receives the final
emphasis. The sentence can appear first in an answer that recommends an
action.

### E303 Let context carry what the reader already knows

When the context already tells the reader which one you mean, use the
bare noun, without a "that" clause or an "of" phrase. The bare noun names
the same concept, so it keeps the term consistent under
[P501](../SKILL.md#p501-keep-terms-consistent).

## 4xx Sentence

### E401 Keep relative that

**Application.** Keep the object relative pronoun "that" even when grammar
allows omission. It marks a clause that describes a noun and uses that
noun as its object. Use other relative pronouns when grammar or meaning
requires them.

**Reason.** The explicit pronoun marks the clause boundary and helps
readers identify the sentence structure.

**Example.**

| Form | Sentence |
| --- | --- |
| Preferred | The report that the server generated contains three errors. |
| Grammatically valid, but avoid here | The report the server generated contains three errors. |

In both sentences, the report is the object of "generated."

### E402 Keep subjects and verbs close without distortion

**Application.** Keep subjects and verbs close when doing so preserves
intent, logical structure, and emphasis. Treat distance as a clue to
possible difficulty, not as a mandatory reason to edit. Follow
[P701](../SKILL.md#p701-keep-the-meaning-you-were-not-asked-to-change).

**Reason.** A long interruption can delay the main action. Moving that
interruption can also change the weight of supporting details.

**Example.**

> The server, which runs in a private network and accepts requests only
> from internal clients, validates each request.

The validation is the main claim. Making the network details a separate
opening sentence gives those details more emphasis. Choose an option that
preserves the intended structure:

- Keep the original sentence.
- State the validation claim first and give the network details afterward.
- Move the network details to a section that explains the network.

## 5xx Lexicon

### E501 Use familiar language

**Application.** Use familiar words and standard sentence structures when
they preserve meaning. Follow
[P501](../SKILL.md#p501-keep-terms-consistent) and
[P502](../SKILL.md#p502-use-the-terms-readers-in-the-field-use) for technical terms and
exact product names.

**Reason.** Familiar language lets readers focus on the content rather
than spend attention interpreting the expression.

**Example.** Use "use" instead of "utilize" when both express the intended
meaning.

### E502 Avoid culture-dependent idioms

**Application.** Generally avoid idioms and metaphors that require
familiarity with English-speaking cultures. Allow metaphors that readers
can understand from the passage's context and that help the explanation
or voice.

**Reason.** An idiom can require knowledge that the passage does not
provide, even when each word is familiar.

**Example.** Use "We gave the migration a lower priority" instead of
"We put the migration on the back burner."
