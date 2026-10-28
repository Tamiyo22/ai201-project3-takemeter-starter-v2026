


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

| Label      | What it means                                                                                               |
| ---------- | ----------------------------------------------------------------------------------------------------------- |
| `analysis` | argues a point and backs it with something checkable                                                        |
| `hot_take` | gives a verdict or ranking with no checkable support                                                        |
| `reaction` | voices how the poster felt right after watching or hearing something, without arguing a claim               |
| `question` | exists to get something back from the community: an answer, an identification, a recommendation or opinions |

It is meant as a first-pass sorter, so someone skimming the sub can find the posts worth reading. A wrong label costs a few seconds of skim time, so the goal is useful for triage, not reliable enough to act on automatically.

Very long lists or essays, news and announcements, and posts with no text were left out on purpose, so the model only sees the four types above.

---

## Label Taxonomy

### `analysis`

**Definition:** Makes a claim and supports it with a specific, checkable detail (a named scene, line, credit, date, number, or a comparison to a named work) offered as the reason.

**Example 1:**

> Hokum has some of the most unique scares I've seen from a horror movie in a while. […] I hate the overuse of jumpscares in horror movies atm, so Hokum's slow, silent panning to a particular scare was very exciting, like when Ohm was trying to turn off the tv when a figure appears in the reflection after it turns off. […] Same with the beginning scene with the girl on the stairs which I thought effectively set the tone for the rest of the film.

**Example 2:**

> Finally watched Obsession! […] Nothing has disturbed me as deeply as this film. The not so subtle subtext of date rape and Bear's predatory adoration is deeply unsettling […] One of the creepiest scene to me in horror filmography is the "black maid" Georgina crying and saying "No" on repeat in Get Out that's basically the whole shtick with Nikki.

### `hot_take`

**Definition:** A confident verdict, ranking or recommendation with no support offered. It might be true, but it isn't argued.

**Example 1:**

> Martyrs is one of the best horror movies ever made. Martyr's violence and philosophical questions long stayed with me after the credits rolled. Despite being so unforgiving, it has something that's so rare to find in other movies, in a sense it's beautiful. Don't even get me started on that ending..

**Example 2:**

> BONE TOMAHAWK (2015). It's AWESOME. It may look like just a western from a distance, but damn the horror vibes are strong. Disturbing, but well worth the ride.

### `reaction`

**Definition:** An immediate response to something that just happened, mostly feeling and not a verdict. It needs a timing cue ("just watched", "tonight") and no ranking ("best of the decade" makes it a `hot_take`).

**Example 1:**

> Watching Creep (2014) for the first time. It's about 10 minutes in and I'm already very uncomfortable. 😆

**Example 2:**

> Goodnight 💤 from Demon Mom in Mr Sandman 2024 💀. Talk about a Creepy possessed Demon. Not the best idea to watch this flick in the dark right before bed. Unless you want nightmares. This movie messed me up ..I Watched Mr sandman 2024 on Tubi n creeped me out bigtime

### `question`

**Definition:** The post exists to get something back from readers: an identification, a recommendation, an answer, or their opinions.

**Example 1:**

> am i reaching or does the colour red symbolize something in annabelle creation? the red glass, red record player, annabelle's ribbon etc.

**Example 2:**

> What horror movie genuinely scared you as a kid and still haunts you today? I'm curious to hear everyone's personal horror stories. Which movie gave you nightmares as a kid and still makes you uneasy now? Was it the story, a character, or just the atmosphere?

### The hardest boundary

**Which two labels:** `question` vs `hot_take`. Many posts state a strong opinion and then end with "Anyone else?" or "Thoughts?".

**The decision rule I used every time:** Delete the closing ask. If what's left still works as a statement, the ask was tacked on and the post is a `hot_take` (or whichever label the rest earns). If what's left is pointless without the ask ("Has anyone seen Good Boy?"), the ask was the point and it's a `question`. Rhetorical questions ("Can we all agree X is the best?") don't count as asks. The full ordered tests (question, analysis, reaction, hot_take) are in `LABELING_RULES.md`.

---

## The Dataset

**Where the posts came from:** r/HorrorMovies, collected in October 2026. Reddit blocks scripts with an HTTP 403, so I opened listing pages in my browser and saved them as .json. 308 posts were pasted in as text and 270 more came from six of those JSON listing files (404 listings, 310 unique post ids). Each post's title and body are joined into one line, with HTML entities, URLs and zero-width characters cleaned up. Duplicates were removed by post id, exact text, and near-duplicate text. 21 JSON posts were dropped (long lists or essays, news and announcements, posts with no text).

**How I labelled them:** 16 rows are marked `cold` in the note column (labeled by me with no help). `pre-labeled` rows (about 292) were labeled first by Claude from my four definitions. After that I asked whether the labels were good, and Claude wrote tie-break rules (`LABELING_RULES.md`), blind-relabeled a random 60 rows (88% agreement, kappa 0.82, same labeler so an upper bound), and re-read about 290 flagged rows, changing 51 labels. Every changed row says `v2: was <old label>` in its note, and `labels_v1.csv` keeps the first version. About 280 unflagged rows (mostly short hot_takes and clear questions) were not individually re-read in v2.

**Counts per label:**

| Label     | Count | Share |
| --------- | ----- | ----- |
| hot_take  | 238   | 41.2% |
| question  | 228   | 39.4% |
| analysis  | 93    | 16.1% |
| reaction  | 19    | 3.3%  |
| **Total** | 578   | 100%  |

The labels follow `LABELING_RULES.md`, which applies four tests in a fixed order (question, analysis, reaction, hot_take). `reaction` is thin (19 rows, about 3 land in each test split), so its score will jump between seeds. It also fails my own criterion 3 (at least 40 rows per label).

**Three hard cases**

**1.**

> _The post:_ "This is the scariest movie I've ever seen. I haven't slept for days, I watched this movie for the first time a few days ago 😭 […] I flew like Usain Bolt to turn the lights on after the movie was done, and slept with all the lights on in the house."
>
> _Could have been:_ `reaction` vs `hot_take`
>
> _I chose:_ `hot_take`, because the title is a superlative verdict ("scariest ever") and the "few days ago" timing means it isn't an immediate response, even though the feeling is strong.

**2.**

> _The post:_ "Rewatched this classic last night. Any fright night fans here? This is my favorite horror classic of all time […] Is it 'scary' compared to today's horror movies?, No. But it sure is an amazing classic."
>
> _Could have been:_ `question` vs `hot_take`
>
> _I chose:_ `hot_take`, because after deleting "Any fright night fans here?" the rest still stands as a verdict. v1 had it as `question`.

**3.**

> _The post:_ "The Descent (2005) is still a masterclass in tension. […] They used such a limited palette, but it looks incredible. It's rare to find a horror movie with an all-female cast that feels this gritty and grounded without falling into tropes."
>
> _Could have been:_ `hot_take` vs `analysis`
>
> _I chose:_ `hot_take`, because the details (limited palette, all-female cast) are mentioned but never used as the reason for the claim; the support is adjectives ("gritty", "grounded").

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased` (the notebook default)

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post, seed 42. Trained on: `cpu` (CPU), torch 2.14.1+cpu, as recorded in `results.json`. The three epochs (78 steps) took about 6 minutes 21 seconds.

**Anything I changed from the defaults, and why:** I did not change any hyperparameters. The only edit was the label list in section 2, which is now `["analysis", "hot_take", "reaction", "question"]` so it matches the four labels in `labels.csv`.

**Split sizes:** The notebook's stratified 70/15/15 split of the 578-row `labels.csv` gives 404 train / 87 validation / 87 test. Test split per label: hot_take 36, question 34, analysis 14, reaction 3. `reaction` has far fewer than the 8 the brief warns about, and `analysis` is also small, so their F1 scores will jump between seeds.

| label    | train | val | test |
| -------- | ----- | --- | ---- |
| analysis | 65    | 14  | 14   |
| hot_take | 166   | 36  | 36   |
| reaction | 13    | 3   | 3    |
| question | 160   | 34  | 34   |

**What the run produced:** Training loss fell from 1.152 to 0.849 and validation loss from 1.077 to 0.847 over the three epochs; validation accuracy rose from 0.586 to 0.736 and validation macro F1 from 0.319 to 0.408. On the 87 test posts (seed 42) the saved `results.json` has accuracy 0.678 and macro F1 0.375. The model never predicted `analysis` or `reaction` on the test split, so both have an F1 of 0.000, and `hot_take` (0.730) and `question` (0.771) carry the score. Accuracy on the most confident third of predictions was 0.862 against 0.483 on the least confident third. `results.json` and `test_split.csv` are committed.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- _What I asked for:_ I gave Claude my pasted CSV and the six Reddit JSON files and asked it to combine them, clean up the JSON, make sure every post was unique, and label everything using my four definitions.
- _What came back:_ One CSV with 578 unique posts, the JSON text cleaned up (no links, HTML or stray characters), and a label and note on every row.
- _What I changed:_ I used that file as the base for my dataset and kept the `pre-labeled` notes so it's clear which rows Claude labeled.

**Moment 2**

- _What I asked for: Label all the rows based on my label definitions.
- _What came back:_ 558 rows of labeled data.
- _What I changed:_ I kept the labels and rows as written.

**Pre-labelling disclosure:** Claude pre-labeled rows (marked `pre-labeled` in the note column), including all the posts that came from the JSON files, and then relabeled flagged rows under the v2 rules. 16 rows marked `cold` were labeled by me with no help. About 280 rows that Claude did not flag were not individually re-read in v2.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure          | Baseline | Trained | Difference |
| ---------------- | -------- | ------- | ---------- |
| Overall accuracy | 0.299    | 0.678   | +0.379     |
| Macro F1         | 0.255    | 0.375   | +0.120     |
| F1 — `analysis`  | 0.274    | 0.000   | -0.274     |
| F1 — `hot_take`  | 0.000    | 0.730   | +0.730     |
| F1 — `question`  | 0.545    | 0.771   | +0.226     |
| F1 — `reaction`  | 0.200    | 0.000   | -0.200     |

**What I predicted before I looked:** I can't give a true blind prediction here, because I had already seen the trained model's numbers from unit 5 (accuracy 0.678, and it never predicted `analysis` or `reaction`) before I ran the baseline. What I expected from that was that the trained model would beat the baseline on `hot_take` and `question`, my two biggest labels, and that the baseline might do better on `analysis` and `reaction`, which the trained model never predicted.

**What the gap actually means:** The trained model is far more accurate overall (0.678 vs 0.299), and most of that comes from `hot_take`, where the baseline scored an F1 of 0.000 on 36 posts. Its accuracy is below 0.414, what I'd get by always guessing `hot_take`, so without training it is worse than guessing the biggest label. But the trained model's wins come only from the two big labels. The baseline did better on `analysis` (0.274 vs 0.000) and `reaction` (0.200 vs 0.000), the two labels the trained model never predicted. `reaction` has only 3 test posts, so that 0.200 is one post and I won't read much into it. The fine-tuning clearly added something, but it learned the common labels and not the rare ones.

---

## Run Log — Before


| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.62 on every seed and ≥ 0.15 above the always-`hot_take` baseline (0.414) | 0.678 (+0.264 over baseline) | 0.724 (+0.310 over baseline) | 0.690 (+0.276 over baseline) | MET |
| 2. Per-label F1 floors | `question` ≥ 0.75, `hot_take` ≥ 0.55, `analysis` ≥ 0.40, `reaction` ≥ 0.25 on every seed | question 0.771, hot_take 0.730, analysis 0.000, reaction 0.000 | question 0.816, hot_take 0.790, analysis 0.000, reaction 0.000 | question 0.795, hot_take 0.734, analysis 0.000, reaction 0.000 | MISSED |
| 3. Balance | Every label ≥ 40 rows; no label > 50% | reaction has 19 rows; largest label is 41.2% | Same dataset counts | Same dataset counts | MISSED |
| 4. Self-consistency | ≥ 25 of 30 matches when relabeling 30 posts at least 7 days later | Not yet tested | Not yet tested | Not yet tested | NOT YET TESTED |
| 5. Confidence | Most-confident half ≥ 10 percentage points more accurate than least-confident half on every seed | Half comparison pending; thirds: 86.2% vs. 48.3% (gap 37.9 points) | Half comparison pending; thirds: 86.2% vs. 55.2% (gap 31.0 points) | Half comparison pending; thirds: 86.2% vs. 44.8% (gap 41.4 points) | PENDING |

### Confusion matrix

Seed 42:

| true \ predicted | analysis | hot_take | reaction | question |
| ---------------- | -------- | -------- | -------- | -------- |
| **analysis**     | 0        | 8        | 0        | 6        |
| **hot_take**     | 0        | 27       | 0        | 9        |
| **reaction**     | 0        | 1        | 0        | 2        |
| **question**     | 0        | 2        | 0        | 32       |

**My biggest off-diagonal number, and what it means:** 9 real `hot_take` posts were called `question`, and only 2 real `question` posts were called `hot_take`, so on this pair the model leans toward `question`. The bigger problem is that it never predicted `analysis` or `reaction` at all. All 14 `analysis` posts went to `hot_take` (8) or `question` (6), and 2 of the 3 `reaction` posts went to `question`.

---


## Verdicts and Diagnoses

<

| # | Criterion | Target | Verdict | How I decided |
|---|-----------|--------|---------|---------------|
| 1 | Overall accuracy | At least 0.62 on each of three seeds and at least 0.15 above the majority-class baseline | MET | Accuracy was 0.678 (seed 42), 0.724 (seed 7), and 0.690 (seed 2024). All exceeded 0.62 and beat the 0.414 baseline by at least 0.264. |
| 2 | Per-label F1 | `question` ≥ 0.75, `hot_take` ≥ 0.55, `analysis` ≥ 0.40, `reaction` ≥ 0.25 on every seed | MISSED | `question` and `hot_take` met their thresholds on all seeds, but `analysis` and `reaction` had F1 scores of 0.00 on all three seeds. |
| 3 | Label coverage and balance | At least 40 examples per label, with no label exceeding 50% of the dataset | MISSED | `reaction` had only 19 examples, below the minimum of 40. The largest class, `hot_take`, represented 41.2% of the 578 examples, meeting the 50% limit. |
| 4 | Delayed relabel consistency | Relabel 30 random posts at least 7 days later and match at least 25/30 original labels | NOT YET TESTED | The required delayed relabeling result is not available yet. The earlier same-day relabeling result does not satisfy the 7-day requirement. |
| 5 | Confidence-based accuracy | On every seed, the most-confident half of test predictions is at least 10 percentage points more accurate than the least-confident half | PENDING | The current results compare the most-confident and least-confident thirds, with accuracy gaps of 37.9, 31.0, and 41.4 percentage points for seeds 42, 7, and 2024. The required half-versus-half comparison has not yet been calculated. |


**Diagnoses**

Criterion 2 — Per-label F1 (MISSED). The model consistently failed to identify analysis and reaction, scoring 0 F1 for both labels across all three seeds. The seed-42 confusion matrix confirms that the model never predicted either label. reaction is particularly data-limited: it has only 19 examples in the full dataset and just 3 in the seed-42 test set. Too few examples is therefore a strong likely cause for reaction. However, analysis has 93 examples and still scored 0 F1, so the problem may also involve the model struggling to distinguish that category from the other labels. The 30/30 agreement result supports consistent labeling in the compared sample, making inconsistent labeling less likely as the explanation for that sample's results.

Criterion 3 — Label balance (MISSED). The dataset has only 19 reaction examples, fewer than the required 40. This is direct evidence that the class has too few examples. Although no class exceeds 50% of the dataset, the model's failure to predict analysis and reaction shows that meeting the maximum-class threshold alone does not ensure the model learns every label. 

Criterion 4 — Labeling self consistency. (Pending)

Criterion 5 — Confidence separation (PENDING). The seed-42 result shows that the most-confident third was substantially more accurate than the least-confident third: 86.2% versus 48.3%, a 37.9-percentage-point difference. This is encouraging evidence that confidence carries useful information. However, the criterion specifically requires comparing the most-confident half with the least-confident half across all three seeds, so the available numbers do not establish whether the target was met.

---

## Agreement Report

**Agreement rate:** ** 30/ 30 = 100**%

**Disagreements**

There were none, so there is nothing to adjudicate and none of the three piles ((a), (b), (c)) apply.

**1.**

> _The post:_ sp_014: "Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."
>
> _Staff said / I said:_ Staff said `hot_take`, I said `hot_take`. No disagreement.
>
> _My call, and why:_ `hot_take`. The 3% is checkable, so it could be read as `analysis`. But the conclusion is already stated ("obviously... the whole story"), and the number is decoration on it. That is the staff's own rule 1 example, so I treated it as the clearest case of the rule.
>
> _Which pile:_ None, since we agreed. If I had called it `analysis`, it would have been pile (a): the rule covers it and I would have applied it loosely.

**2.**

> _The post:_ sp_010: "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> _Staff said / I said:_ Staff said `analysis`, I said `analysis`. No disagreement.
>
> _My call, and why:_ `analysis`. It is a tiny, hedged sample and could be read as a `hot_take` about shoes. But the observation is checkable and the claim rests on it. Rule 1 asks whether the fact carries the argument, not whether the evidence is strong.
>
> _Which pile:_ None, since we agreed. If I had called it `hot_take`, it would have been pile (c): the rule is ambiguous on weak evidence, and a reading could be defended.

**What the pattern in my disagreements tells me:**
With no disagreements, the check can't tell a labeling problem from a model problem for my own data, which is what it's supposed to do in Milestone 4. Three things limit what 30 of 30 means. First, staff marked 7 of the 30 posts as borderline (sp_005, sp_010, sp_014, sp_019, sp_020, sp_028, sp_029), and all 7 matched, which suggests the three rules are tight in this set. Second, the rule text's own example ("times are down 3% since 2017…") is almost the same as sp_014, so that post was close to given away. Third, 30 posts is a small set, and this is a running forum with three labels, not my horror-movie data with four. The result says nothing about how consistent my 578 labels are. The only consistency numbers I have for them are the 88% blind relabel from unit 5 (same labeler, so an upper bound) and the relabel check for criterion 4

---

## The Improvement

**What I changed:**
I simplified the classification labels from four classes (analysis, hot_take, reaction, and question) to two classes: statement and question. I combined analysis, hot_take, and reaction into statement so the model could focus on distinguishing posts that express an opinion or analysis from posts that ask the community for information or recommendations.

**Which diagnosis pointed at it:**
The original model struggled to learn the smaller classes, particularly analysis and reaction, which had F1 scores of zero. The class imbalance and difficulty distinguishing between similar types of statements suggested that merging related labels into a broader statement class could improve performance.


### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Accuracy | >= 0.71 and >= 10 percentage points above baseline (0.606) | 0.885 | 0.885 | 0.862 | PASS |
| 2. Per-class F1 | Both classes >= 0.70 | Statement: 0.904; Question: 0.857 | Statement: 0.906; Question: 0.853 | Statement: 0.889; Question: 0.818 | PASS |
| 3. Class balance | At least 150 examples per class; neither class > 65% | Statement: 350 (60.6%); Question: 228 (39.4%) | Statement: 350 (60.6%); Question: 228 (39.4%) | Statement: 350 (60.6%); Question: 228 (39.4%) | PASS |
| 4. Relabel consistency | Relabel 30 random posts after 7+ days; at least 25/30 labels match | Relabeled all data; original labels unavailable for comparison | Relabeled all data; original labels unavailable for comparison | Relabeled all data; original labels unavailable for comparison | FAIL |
| 5. Confidence separation | Most-confident half is at least 10 percentage points more accurate than least-confident half | Most: 1.000; Least: 0.791; Gap: 0.209 | Not calculated | Not calculated | PARTIAL |

**Did it help, and how do I know:**

Yes, the change substantially improved the model's ability to recognize both categories. All three seeds achieved accuracy between 86.2% and 88.5%, and both labels exceeded the required F1 score of 0.70 on every seed. The dataset also meets the revised balance requirements. However, the delayed relabeling criterion was not met because I relabeled the entire dataset rather than preserving the original labels for comparison. Confidence separation passed for Seed 42, with a 20.9-percentage-point gap between the most-confident and least-confident halves, but it still needs to be calculated for Seeds 7 and 2024.

---

## What's Still Broken


**The gap between what I meant my labels to capture and what the model
learned:**

The Seed 42 confusion matrix shows that the model misclassified 6 statement posts as questions and 4 question posts as statements. This suggests that the model sometimes struggles to distinguish between posts that express an opinion or analysis and posts that seek information or recommendations. Although the overall results are strong, these errors show that the model does not always correctly identify the author's primary intent, particularly when a post's purpose is ambiguous.

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
