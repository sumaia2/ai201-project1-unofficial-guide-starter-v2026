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

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
