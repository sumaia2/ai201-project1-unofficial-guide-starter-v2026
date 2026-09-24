# The Unofficial Guide

**Sumaia Ali — corpus: campus_life**

---

# Unit 1

## What This Does

This system answers questions about student life at a fictional campus, using
88 short posts covering topics like dining halls, housing, on-campus jobs, and
course logistics. It's built for specific, factual questions — like dining
hall hours, housing costs, or how many hours students can work on campus — and
answers only from what's actually in those documents, naming its source. If a
question falls outside what the corpus covers, it says so instead of guessing.

## Chunking Strategy

**Chunk size:** paragraph-based (no fixed character count), merged up to a 100-character minimum
**Overlap:** none (paragraph splits are natural, non-overlapping boundaries)

The starter's fixed 800-character chunker barely touched this corpus — 88
documents became 88 chunks, because almost no post crosses 800 characters. But
reading the documents in Milestone 1 showed that a single post often holds two
or three genuinely separate ideas (e.g. a personal anecdote, then a distinct
block of hours/cost facts). Splitting on blank-line paragraph breaks instead of
a character count keeps each thought whole while still separating them where
it matters. Paragraphs under 100 characters get merged into a neighboring one
so a short heading or fragment never becomes its own thin, useless chunk. This
produced 143 chunks (up from 88), averaging 194 characters, which matches how
short these documents naturally are.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.


**Chunk 2** — source: `course_cs_340.txt#0` — produced by: `chunker.py::split_documents`

CS 340 Databases

I'm a junior and I've done this twice now. Format is lecture twice a week plus a project that runs the whole term. Assessment: one midterm and a final, both open-book. Lightly curved, usually two or three points.


**Chunk 3** — source: `course_phys_130_exams.txt#0` — produced by: `chunker.py::split_documents`

PHYS 130 Mechanics — assessment

Three midterms, no final, plus a lab practical. Not curved, but the lowest midterm is dropped.

The lab practical is worth 20% and almost nobody prepares for it.


**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#1` — produced by: `chunker.py::split_documents`

Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.


**Chunk 5** — source: `housing_morrow_house.txt#1` — produced by: `chunker.py::split_documents`

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

The bad: known damp problem on the ground floor; two rooms were taken offline in 2024.


## Sample Answer

**Question:** What are Halden Hall's hours and cost?

**Answer:**

Halden Hall's hours are 7:30am to 7:00pm on weekdays, and it is closed on
Sundays. The cost is one meal swipe or $10.00 cash (dining_halden_hall.txt).

Source: dining_halden_hall.txt


**My relevance cutoff:** 0.6 (kept the starter's default)

I ran my 5 in-scope test questions and the 5 OUT_OF_SCOPE questions and recorded
the best distance for each. The two groups separated cleanly with a wide gap
(0.392 to 0.803, no overlap), so the starter's default of 0.6 already sits
comfortably in the middle — I didn't need to change it.

| Question | In corpus? | Best distance |
|---|---|---|
| What are the wait times like at Halden Hall dining? | Yes | 0.195 |
| What are Halden Hall's hours and cost? | Yes | 0.340 |
| What kind of housing is Tamsin Court and what year was it built? | Yes | 0.259 |
| What's the downside of living in Tamsin Court? | Yes | 0.392 |
| How many hours a week can students work on campus, and what's recommended? | Yes | 0.316 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.923 |
| Who won the 1994 World Cup? | No | 0.874 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.803 |
| How do I write a for loop in Rust? | No | 0.877 |

## How I Used AI

**1.** I asked Claude to help me write a custom chunking strategy after seeing
that the starter's fixed-size chunker wasn't splitting my corpus at all (88
docs → 88 chunks). Claude suggested paragraph-based splitting with a minimum
character merge threshold. I reviewed the output chunks myself to confirm they
each held complete thoughts before committing.

**2.** I asked Claude to help me interpret my distance scores when setting the
relevance cutoff in Milestone 4. I gave it my 10 recorded distances (5 in-scope,
5 out-of-scope) and asked where the gap was. It confirmed the starter's default
of 0.6 already sat well inside the gap, so I kept it rather than changing
`config.py` unnecessarily.

**3.** I asked Claude to help implement hybrid search (BM25 + semantic) after
diagnosing that a pure-semantic retrieval failure was causing one of my
questions to miss. The first implementation had two bugs I didn't catch
myself: an indentation error that caused `search()` to return after only one
candidate, and a normalization approach that rescaled semantic distances
relative to each query's candidate pool, which broke the relevance gate
(0 of 5 out-of-scope questions refused instead of 5 of 5). I used Claude to
help trace both bugs by writing small debug scripts and reading raw
candidate lists directly, and the second bug taught me that distance
normalization needs to preserve absolute calibration, not just relative
ranking within one query.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Distance gap ≥ 0.15 between groups | 0.15 | 0.56 | 0.56 | 0.56 | MET |

Produced by `run_eval.py::main`, retrieval from `store.py::search`, chunks
from `chunker.py::split_documents`. Full output in
`results/run_2026-09-23_2000_before.md`.

Real output — the one failing question, "What's the downside of living in
Tamsin Court?" (failed all 3 runs):

Based on the provided documents, there is no mention of a downside or
negative aspect to living in Tamsin Court (the documents only mention that
it has studio apartments with private kitchens and bathrooms, and detail its
laundry machine ratio).

Source: housing_tamsin_court.txt and housing_tamsin_court_laundry.txt


Real output — a passing question, "What are Halden Hall's hours and cost?"
(passed all 3 runs, representative of the other 4):

Halden Hall's hours are 7:30am to 7:00pm on weekdays, and it is closed on
Sundays. It costs one meal swipe or $10.00 cash.

Source: dining_halden_hall.txt


Out-of-scope gate — refused 5 of 5, produced by `run_eval.py::check_out_of_scope`:

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.923 | refused |
| Who won the 1994 World Cup? | 0.874 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.803 | refused |
| How do I write a for loop in Rust? | 0.877 | refused |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | 4 of 5 questions answered correctly with the fact present, across all 3 runs, both before and after the improvement. The 5th (Tamsin Court downside) failed all 3 runs in both rounds — the mechanism changed (pure retrieval miss → generation picking the wrong of two present facts) but the numeric outcome stayed 4/5. |
| 2 | Every answer names a source | MET | All 5 questions named at least one source file in all 3 runs, in both before and after rounds, including the incorrect Tamsin Court answer, which still cited a real (if not ideal) source. |
| 3 | Gate stops out-of-corpus questions | MET | Before: 5 of 5 refused. After: 4 of 5 refused — one question (ibuprofen dosage, distance 0.588) slipped under the 0.6 cutoff once hybrid scoring compressed the distance gap. Still meets the 4-of-5 target, but the margin shrank and is worth flagging as a real regression. |
| 4 | Chunks read as complete thoughts | MET | 5 of 5 sampled chunks in Milestone 3 (Unit 1) were complete, self-contained thoughts. Unchanged in Unit 2 since the chunker itself was not the improvement made. |
| 5 | Distance gap ≥ 0.15 between in-scope and out-of-scope groups | MET | Before: 0.56 gap (0.30 avg in-scope vs 0.86 avg out-of-scope). After: 0.33 gap (in-scope average rose, out-of-scope average fell, as hybrid scoring pulled both groups' distances downward and closer together). Still clears the 0.15 target, but with much less margin than before. |

## Diagnoses

### Criterion 1 — "What's the downside of living in Tamsin Court?" (failed all 3 runs, before fix)

**Stage: Retrieval**

The answer exists in the corpus — `housing_tamsin_court.txt#1` contains "The
bad: the most expensive tier by a wide margin, and isolating if you're new."
My chunker splits this into its own chunk, separate from the "studio
apartments with private kitchen" intro chunk in the same file.

The top-5 retrieved chunks for this question never included the "good/bad"
chunk at all — instead they pulled chunks from *other* dorm files
(`housing_fenwick_court.txt`, `housing_morrow_house.txt`,
`housing_old_brewhouse.txt`) that happened to share similar generic
"downside" language. This is a retrieval ranking problem, not a chunking
problem: the right chunk exists and is intact, but competing chunks about
the same *topic* (dorm downsides in general) outranked it for this specific
document, because pure semantic embedding doesn't weight the proper noun
"Tamsin Court" heavily enough against the generic phrase "downside of
living."

**Pattern check:** this is the only miss in the "before" run, so there's no
cross-question pattern yet — but it points at a general risk: when several
documents share similar generic sentence structure ("the good:", "the bad:"),
pure semantic similarity can retrieve the wrong document's version of that
pattern instead of the one actually asked about.



## The Improvement

**What I changed:** Added hybrid search — BM25 keyword scoring blended with
the existing semantic (cosine) distance, in `store.py`. Retrieval now pulls
a wider candidate pool (top_k × 4, minimum 20) from Chroma, scores that pool
with BM25 against the raw question text, and combines both scores into a
single distance (70% semantic, 30% BM25 — `config.HYBRID_BM25_WEIGHT = 0.3`).
I also raised `TOP_K` from 5 to 8 to give the blended ranking more room to
surface a correct chunk that wasn't already in the strict top 5.

**Why I picked it:** My Milestone 3 diagnosis pointed directly at this: the
failure was that a distinctive proper noun ("Tamsin Court") wasn't weighted
strongly enough by pure semantic embedding, letting chunks from unrelated
documents about a similar *topic* outrank the correct document. BM25 rewards
exact keyword/term overlap, which is exactly the signal semantic search was
missing for this kind of question.

**What actually happened (worth reporting honestly):** My first
implementation had two real bugs, both instructive:

1. An indentation error caused `search()` to `return` from inside the
   candidate loop, so only the first Chroma result was ever collected before
   BM25 re-ranking ran on a pool of one. Fixed by dedenting the return
   statement outside the loop.

2. My normalization approach rescaled *both* BM25 and semantic distance to
   0-1 relative to each query's own candidate pool. This meant even a
   completely irrelevant question (e.g. "What is the capital of Mongolia?")
   would have its best-matching candidate rescaled down near 0, since
   min-max normalization always produces a "best" and "worst" regardless of
   whether either is actually relevant. This broke the relevance gate
   completely — 0 of 5 out-of-scope questions were refused, down from 5 of 5.
   Fixed by leaving the semantic distance in its original, calibrated cosine
   scale and only normalizing BM25's unbounded score before blending.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 4. Chunks read as complete thoughts | 4 of 5 | 5/5 | 5/5 | 5/5 | MET (unchanged — chunker untouched) |
| 5. Distance gap ≥ 0.15 | 0.15 | 0.33 | 0.33 | 0.33 | MET |

Real output (Tamsin Court downside question, after fix):

Based on the provided documents, the downside of living in Tamsin Court is
that the ratio of washers to dryers is wrong (eight washers and six dryers
for the building), which causes the dryers to back up and creates wait times
on Sunday evenings.

Source: housing_tamsin_court_laundry.txt


**Did it help?** Partially, with a real trade-off — reported honestly rather
than smoothed over.

Criterion 1 stayed numerically at 4/5, but the *reason* changed: the correct
document (`housing_tamsin_court.txt`) and its "good/bad" chunk are now
reliably retrieved, which they weren't before. However, the model now has
*two* true "downside" facts in context (the cost/isolation one and the
laundry-ratio one) and consistently picks the laundry one — a generation-stage
issue that retrieval alone couldn't fix.

Criterion 3 got measurably worse — 5/5 dropped to 4/5. Blending BM25 into the
score compressed the gap between in-scope and out-of-scope distances (0.56 →
0.33), letting one borderline out-of-scope question (ibuprofen dosage, 0.588)
slip under the 0.6 cutoff that was calibrated for pure semantic distance, not
the new blended one.

Net: hybrid search fixed the specific retrieval failure it was diagnosed to
fix, but at a real cost to a different criterion — the honest verdict is
"helped one thing, cost another," not "improved the system."

## What's Still Broken

**Criterion 1 (retrieved chunk contains the answer) — still 4/5, unresolved root cause.**
The "downside of living in Tamsin Court" question still fails, though the
mechanism changed. Before hybrid search, the right chunk never made it into
context at all. After hybrid search, the right chunk (`housing_tamsin_court.txt#1`,
"the bad: the most expensive tier... isolating if you're new") IS retrieved,
but the model consistently answers with a different, real downside from a
sibling document (`housing_tamsin_court_laundry.txt`) instead. This is a
generation-stage problem now, not a retrieval-stage one: when multiple
plausible "downside" statements exist across retrieved chunks, the grounding
prompt doesn't push the model toward the most central one from the specific
building being asked about.

What I'd try next: tighten the grounding prompt to prefer facts from the
document whose filename most closely matches the entity named in the
question, or add a step that ranks retrieved chunks by whether the question's
key entity (e.g. "Tamsin Court") appears in the *chunk text itself*, not just
in the source filename. I stopped here because that's a generation-prompt
change, not the one improvement this unit allows me to make and measure.

**Criterion 3 (gate stops out-of-corpus questions) — regressed from 5/5 to 4/5.**
Blending BM25 into the distance calculation compressed the separation between
in-scope and out-of-scope distance groups (gap dropped from 0.56 to 0.33).
One out-of-scope question (ibuprofen dosage, distance 0.588) now slips just
under the 0.6 cutoff. The mechanism: BM25's keyword overlap can accidentally
reward generic words shared between an out-of-scope question and campus_life
chunks (e.g. "recommended," "students"), nudging the blended distance down
even when the content is unrelated.

What I'd try next: re-measure and raise the cutoff specifically for the
hybrid-scored system (my in-scope/out-of-scope gap analysis was calibrated
for pure semantic distance, not the blended score) — something in the 0.62-0.65
range would likely restore the 5/5 refusal rate without meaningfully hurting
recall on real questions. I stopped here because Milestone 4 only allows one
change per unit, and I'd already spent it on hybrid search itself.

## What I'd Do Differently

If I were writing these five criteria again, I'd change criterion 1. "The
retrieved chunks include one that contains the answer" turned out to hide an
important distinction: a chunk can technically contain relevant material
without being the *right* material for what was actually asked. My Tamsin
Court downside question passed retrieval (the correct chunk was in context)
but still produced a wrong answer, because a different chunk containing a
different true fact competed for the model's attention. I'd rewrite it as
something like "the model's final answer matches the specific fact my
`expects` field names, in at least 4 of 5 questions" — which tests the whole
pipeline's output, not just whether the right material happened to be present
somewhere in context.

I'd also set criterion 3's target more conservatively from the start. My
original in-scope/out-of-scope gap (0.56) looked so wide that I assumed any
reasonable change would leave the gate intact. Hybrid search showed that
assumption was fragile — a technique that changes the distance formula can
compress that gap without necessarily reflecting a worse understanding of
relevance. I'd have benefited from stating up front that any retrieval change
needs the cutoff re-measured, not just re-used from Unit 1.
