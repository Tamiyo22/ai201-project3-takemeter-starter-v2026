# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. _"The model is accurate"_ is an
opinion. _"Every label has an F1 of at least 0.60 on the held-out set"_ is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — _"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"_. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area                  | A question it could answer                                            |
| --------------------- | --------------------------------------------------------------------- |
| Overall accuracy      | How often does it need to be right to be worth using?                 |
| Per-label performance | Is one label allowed to be much worse than the others?                |
| Balance               | How lopsided can your label counts get before it's a problem?         |
| Consistency           | If someone else labelled the same posts, how often should you agree?  |
| Confidence            | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

Overall accuracy on the held-out test set is at least 0.62 on every one of the three seeds, and at least 15 points above the always-predict-the-biggest-label baseline on every seed.

**Why this target:**

I have four labels, so random guessing gets 25%, and my biggest label is hot_take at 41.2%, so a majority guesser lands around 41% (about 0.56 once I add the 15-point gap). With about 87 test rows, one row is about 1 point and a single seed can swing 5 to 8 points either way just from which rows land in the test set. Because the target has to hold on all three seeds, I set it a few points under where I expect the model to land (about 0.66 to 0.70, a guess based on the 88% agreement I measured when I relabeled 60 rows blind), not at it. The 15-point gap rule keeps the target honest if a different split makes one label bigger than the 41% I planned around.

---

## 2.

Every label has an F1 of at least its own floor on every one of the three seeds: question 0.75, hot_take 0.55, analysis 0.40, reaction 0.25.

**Why this target:**

A model that always predicts hot_take scores an F1 of 0 on the other three labels, so each floor has to show the model has actually learned that label. question gets the highest floor because its cues are the clearest in my data (a title prompt, "?", "help me find this movie"). hot_take is my catch-all and the one the other labels leak into, so 0.55. analysis is the boundary I found hardest to label (a claim plus a named, checkable detail, versus an adjective), and it has only about 14 test rows, so one wrong prediction moves its F1 by 0.07 to 0.15. reaction has only 19 rows, so about 3 land in the test set today and its F1 can drop to 0 on a bad seed. Its 0.25 is still about 4 to 6 times what random guessing would score on a label that small, and I expect it to be the criterion I am most likely to miss. Together the floors weigh out to about 0.60, a little under criterion 1 because every label has to clear its floor on every seed.

---

## 3.

Every label has at least 40 labeled rows in labels.csv, and no label is more than 50% of the rows.

**Why this target:**

With a 70/15/15 split, 40 rows leaves 6 in the test set and about 28 in training, which is the fewest examples where a per-label score still means anything. Today the largest label is 41.2%, so the 50% ceiling passes. **The 40-row floor fails today:** reaction has 19 rows, so I need about 21 more reaction posts before the final training run. The 50% ceiling is stricter than the 70% the unit asks for, because at 50% a majority guesser already gets close to my accuracy target in criterion 1, and the criterion would stop telling me anything. I expect reaction to stay the label at risk, because only a small share of posts are written right after watching and mostly voice feeling.

---

## 4.

When I relabel 30 randomly chosen posts at least 7 days after I first labeled them, I match my original label on at least 25 of the 30 (0.83).

**Why this target:**

I have no second labeler, so I test against myself, and the 7-day wait is there so I am not just remembering my answers. A classifier can't be more consistent than the labels it learns from, so this sets the most noise I'm willing to train on. When I relabeled 60 posts blind from the written rules on the same day, I matched 53 of 60 (88%), so I set 0.83 to allow about 5 points of drift over a week. I picked 0.83, not 0.90, because some boundaries are judgment calls (a verdict written as a question, hot_take versus reaction), and I tightened the rules after labeling my first rows. If I miss it, the fix is to tighten the definitions and relabel the rows that flipped, not to change the model. A second person labeling the same posts would be a stronger test, and I would swap one in if I find one.

---

## 5.

On every one of the three seeds, the most confident half of my test predictions is at least 10 points more accurate than the least confident half.

**Why this target:**

If the model is going to sort posts for a person to skim, its confidence has to mean something, so the predictions it is sure about should be right more often than the ones it isn't. I compare the two halves because a fixed cutoff like 0.80 might leave me with only a handful of predictions to judge on an 87-row test set. Each half is about 43 predictions, so one wrong prediction moves a half by about 2 points and 10 points is a gap of about 4 predictions. That is the noisiest of my five criteria, so I picked a small gap because it has to hold on all three seeds. I expect question posts, with the clearest cues, to be most of the confident half.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
