---
name: humanizing-bilingual-ai-writing
description: "Revises English and Japanese AI-generated or AI-sounding prose so it reads like credible human writing while preserving facts, intent, audience, and bilingual consistency. Use when the user asks to remove \"AI-ness\", humanize, de-template, naturalize, localize, or polish English/Japanese documents, profiles, essays, announcements, emails, website copy, proposals, or paired bilingual text."
---

# Humanizing Bilingual AI Writing

## Core Rule

Make the text sound human by making it more specific, proportionate, and context-aware. Do not fake lived experience, invent details, add unsupported claims, or hide uncertainty.

If the user gives target audience, medium, voice, length, or formality, follow it. If not, infer a conservative professional-natural voice from the source and preserve its purpose.

## Workflow

1. Identify the document type, audience, language, and whether the English and Japanese are paired versions of the same content.
2. Extract facts that must not change: names, dates, numbers, titles, concrete claims, sequence, commitments, legal or medical caveats, and cited evidence.
   - Treat unsupported self-descriptions and marketing claims as tone, not facts: e.g. "highly motivated", "passionate", "innovative", `革新的`, `価値を創造`.
   - If the source contains conflicting facts, do not choose one silently. Mark the conflict for confirmation or preserve it in a short note.
3. Diagnose AI signals before rewriting:
   - Generic thesis framing without concrete stakes.
   - Symmetric lists that feel padded.
   - Repeated transitions such as "moreover", "furthermore", "in conclusion", `まず`, `次に`, `さらに`, `最後に`.
   - Inflated but vague adjectives such as "transformative", "innovative", "重要な", `多様な`, `効果的な`.
   - Meta-commentary about the document itself unless the genre needs it.
   - Overbalanced hedging that avoids a real point.
   - Japanese prose that overuses `〜することができます`, `〜といえるでしょう`, `〜が重要です`, `〜において`, `〜を通じて`.
4. Rewrite around intent, not sentence-by-sentence paraphrase. Combine, cut, reorder, or split sentences when that creates a more natural flow.
5. Keep a small amount of imperfection where appropriate: varied sentence length, direct verbs, concrete nouns, and topic-specific phrasing. Do not add typos or forced slang.
6. Validate against the fact list and the user's requested tone.

## English Revision Rules

Prefer direct, grounded prose:

- Replace abstract openings with the actual point.
- Use specific verbs over padded verb phrases.
- Cut filler such as "it is important to note", "in today's fast-paced world", "plays a vital role", "a wide range of".
- Avoid thesaurus polishing. Natural English is often plainer than AI output.
- Use contractions only when they fit the genre.
- Keep technical terms exact; simplify the surrounding sentence instead.
- Vary paragraph rhythm, but do not make every sentence punchy.

## Japanese Revision Rules

Prefer natural Japanese for the audience and medium, not literal translation:

- Replace stiff nominalizations and `〜すること` chains with direct predicates.
- Cut template phrases such as `本稿では`, `〜について解説します`, `〜といえるでしょう` unless the genre truly needs them.
- Use kanji/kana balance appropriate to the document; avoid making every phrase formal Sino-Japanese.
- Prefer concrete subjects when the source is ambiguous, but do not add facts.
- Use `です・ます` or `だ・である` consistently unless the source intentionally mixes register.
- In business prose, keep politeness without overusing `〜させていただきます`.
- Avoid English-shaped sentence order when revising translated Japanese.

## Bilingual Pair Handling

When both English and Japanese versions are present:

1. Decide whether the target is parallel meaning, natural local versions, or a source/translation relationship.
2. Align factual content first: names, dates, titles, scope, obligations, examples, and claims.
3. Revise each language for its own norms. Do not force matching sentence counts.
4. Preserve intentional differences for audience or culture, but flag accidental mismatches.
5. For names, product terms, and taglines, keep the user's established notation unless asked to localize it.
6. In the final output, place all revised language versions before mismatch notes. Do not insert explanatory notes between the English and Japanese versions unless an inline confirmation marker is necessary to avoid presenting a false fact.

## Output Style

By default, provide the revised text first. Add short notes only when they are useful, such as:

- factual ambiguities you preserved instead of guessing
- bilingual mismatches found and fixed
- places where the requested humanization would require new facts
- conflicts that block a clean final version, with a confirmation marker or question

If the user asks for tracked changes, show concise before/after examples for representative edits rather than explaining every sentence.

For bilingual pairs, output order should be: revised English, revised Japanese, then brief notes or confirmation questions.

## Validation Checklist

Before finalizing, check:

- All facts, numbers, names, conditions, and citations are preserved.
- Unsupported self-descriptions and marketing claims were softened or removed rather than treated as immutable facts.
- Factual conflicts were flagged instead of silently resolved.
- The rewritten text no longer relies on generic AI scaffolding.
- The tone matches the audience and document type.
- English reads like native or fluent professional prose, not paraphrase output.
- Japanese reads as Japanese, not translated English.
- Bilingual versions are factually aligned where they should be aligned.
- No invented anecdotes, credentials, outcomes, or emotional claims were introduced.

## Common Mistakes

- Do not make the text casual just to make it "human" — natural is not the same as informal.
- Do not preserve the original paragraph order when it is the very reason the text feels generated.
