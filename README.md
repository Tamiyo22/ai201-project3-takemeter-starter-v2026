# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts posts from r/HorrorMovies, a movie-discussion subreddit with about 220,000 members, into four types:

Label
analysis argues a point and backs it with something checkable
hot_take gives a verdict or ranking with no checkable support
reaction describes how the poster felt, without arguing a claim
question asks the community something

It is meant as a first-pass sorter, so someone skimming the sub can find the posts worth reading. A wrong label costs a few seconds of skim time, so the goal is useful for triage, not reliable enough to act on automatically.

Posts that aren't opinion or discussion (news, fan art, personal shares, moderator posts) were left out on purpose, so the model only sees the four types above.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:**
Makes a point and backs it with something a stranger could check: a number, a timestamp, or a description of what a scene or technique does. Naming a film or an actor is not enough.

**Example 1:**

> What makes it so disturbing is how calmly he approaches the situation, almost as if he's comparing their grades rather than deciding who should live or die. No violence, no screaming.

**Example 2:**

> Coraline has to agree to getting button eyes, while Bella has to agree to letting the Other Mommy enter her heart.

### `hot_take`

**Definition:**
A ranking, recommendation or quality verdict about a film (best, masterpiece, boring, overrated, favorite, must-watch) with no checkable support, only adjectives or feelings.

**Example 1:**

> Misery is a Masterpiece

**Example 2:**

> Martyrs is one of the best horror movies ever made

### `reaction`

**Definition:**
The post is mainly about the poster's own state or experience (scared, uncomfortable, couldn't sleep, cried), without arguing a claim about the film.

**Example 1:**

> It's about 10 minutes in and I'm already very uncomfortable.

**Example 2:**

> I don’t know if this is strictly horror, but it scared me witless and I couldn’t shake it off for ages.

### `question`

**Definition:**
The main purpose of the post is to ask the community something: for opinions, recommendations, or help identifying a film.

**Example 1:**

> Thoughts on Sinister?

**Example 2:**

> What’s a movie that genuinely terrified you as a kid, even though it wasn’t supposed to be a horror movie?

### The hardest boundary

**Which two labels:**
hot_take and question

Boundary Rows flagged
hot_take / question 25
analysis / hot_take 20
hot_take / reaction 17

**The decision rule I used every time:**
1.Read the title first.
2.If the title is an open prompt with no verdict ("Thoughts on Sinister?", "What is your opinion on this movie"), the post is question, even when the body gives the poster's own opinion.
3.If the title itself holds a verdict, even in question form ("Is X the best…?", "Am I the only one who thinks X is boring?"), the post is hot_take.
4.One exception: a long body that argues a point with described specifics is analysis, because that check comes before the question check.

---

## The Dataset

**Where the posts came from:**
r/HorrorMovies, collected in October 2026. Reddit blocks scripts with an HTTP 403, so I opened the listing pages in my browser and saved them as .json. I used three pages of the sub's top posts of the past year (300 posts) and one page of its newest posts (100 posts). Usernames were left out of the dataset.

**How I labelled them:**

Step Removed Remaining
Collected 400
Mod post, game thread, release list, near-duplicate, and posts under 10 words 25 375
Duplicates between pages 7 368
Left out as not opinion or discussion (news, personal shares, series templates, posts that need an image or video, daily threads) 56 312

**Counts per label:**

Counts per label
Label Count Share
hot_take 144 46.2%
question 121 38.8%
analysis 29 9.3%
reaction 18 5.8%
Total 312 100%

analysis and reaction are small because most posts in this sub are verdicts and questions, and my definitions are strict about what counts as support and as a feelings-only post. These counts are from the combined file before any changes during review.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**

> _The post:_ What is your opinion on this movie
> "Midsommar is a brilliantly executed psychological horror film, and personally, I found its approach incredibly refreshing and different from what I usually expect from a horror movie."
>
> _Could have been:_ hot_take or question
>
> _I chose, because:_ I chose question, because: the title is an open prompt with no verdict, and my rule is that the title decides, even when the body states a clear opinion.

**2.**

> *The post:*Why are so many horror protagonists aggressively unlikeable?
> "Hokum was probably the most aggregious recent case of this where the main man was so passive aggressive that I instantly stopped caring about him…", followed by a comparison with Lake Mungo and REC.
>
> *Could have been:*question or analysis
>
> *I chose, because:*I chose analysis, because: the body argues a claim and supports it with named films and a described contrast, and my rule checks for support before it checks for a question.

**3.**

> _The post:_ finally watched The Coffee Table
> "wow. this was one of those movies where I had my hand over my mouth and was sitting on the edge of my seat with anxiety and dread. a masterfully bleak film."
>
> *Could have been:*reaction or hot_take
>
> *I chose, because:*I chose hot_take, because: under my original rule, a single verdict word ("masterfully bleak") makes the post a hot_take, even though most of it describes the poster's own state. This rule is why reaction is my smallest label.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- _What I asked for:_
- _What came back:_
- _What I changed:_

**Moment 2**

- _What I asked for:_
- _What came back:_
- _What I changed:_

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure          | Baseline | Trained | Difference |
| ---------------- | -------- | ------- | ---------- |
| Overall accuracy |          |         |            |
| Macro F1         |          |         |            |
| F1 — `label_one` |          |         |            |
| F1 — `label_two` |          |         |            |

**What I predicted before I looked:**

<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**

<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |     |     |     |
| ---------------- | --- | --- | --- |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |

**My biggest off-diagonal number, and what it means:**

<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| #   | Criterion | Target | Verdict | How I decided |
| --- | --------- | ------ | ------- | ------------- |
| 1   |           |        |         |               |
| 2   |           |        |         |               |
| 3   |           |        |         |               |
| 4   |           |        |         |               |
| 5   |           |        |         |               |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** **_ / 30 = _**%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**2.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**What the pattern in my disagreements tells me:**

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**The gap between what I meant my labels to capture and what the model
learned:**

<!-- Two sentences. Your confusion matrix is the evidence. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
