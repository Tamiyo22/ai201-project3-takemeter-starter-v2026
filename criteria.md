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

Overall accuracy on the held-out test set is at least 0.55 on every one of the three seeds, and at least 10 points above the always-predict-the-biggest-label baseline on every seed

**Why this target:**

Why this target: I have four labels, so random guessing gets 25%, and my biggest label (probably question or hot_take) should get a majority guesser somewhere around [fill in from my final counts]. With about 240 labeled rows and a 70/15/15 split, my test set is about 35 rows, so one row moves accuracy by about 3 points and a single run can swing 5 to 8 points either way. Because the target has to hold on all three seeds, I set it a few points under where I expect the model to land (about 0.60), not at it. The 10-point gap rule keeps the target honest if one label turns out bigger than I planned.

---

## 2.

Every label has an F1 of at least 0.40 on every one of the three seeds, except analysis, which needs at least 0.25.

**Why this target:**
A model that always predicts the biggest label scores an F1 of 0 on the other three, so 0.40 means the model has actually learned a label. analysis gets a looser floor because it is my rarest and hardest label (a point plus a described, checkable specific, and most "because" posts in my data give only an adjective as the reason). With about 30 analysis rows, only 4 to 5 land in the test set, so one wrong prediction moves its F1 by 0.1 to 0.2 and it can drop to 0 on a bad seed. 0.25 is still about double what random guessing would score on a label that small.

---

## 3.

Every label has at least 30 labeled rows in labels.csv, and no label is more than 50% of the rows.

**Why this target:**

With a 70/15/15 split, 30 rows leaves only 4 to 5 in the test set, which is the fewest examples where a per-label score still means anything. 30 out of about 240 is roughly 12%. The 50% ceiling is stricter than the 70% the unit asks for because at 50% a majority guesser already gets close to my accuracy target in criterion 1, and the criterion would stop telling me anything. I expect question and hot_take to be big and analysis to be the label at risk of falling under 30.

---

## 4.

When I relabel 30 randomly chosen posts at least 7 days after I first labeled them, I match my original label on at least 24 of the 30 (0.80).

**Why this target:**

I have no second labeler, so I test against myself. A classifier can't be more consistent than the labels it learns from, so this sets the most noise I'm willing to train on. I picked 0.80, not 0.90, because some boundaries are judgment calls (a verdict in question form, hot_take versus reaction), and I tightened my rules after labeling my first 20 rows, so this is the criterion I'm most likely to miss. If I miss it, the fix is to tighten the definitions and relabel the rows that flipped, not to change the model.

---

## 5.

On every one of the three seeds, the most confident half of my test predictions is at least 10 points more accurate than the least confident half.

**Why this target:**

If the model is going to sort posts for a person to skim, its confidence has to mean something, so the predictions it is sure about should be right more often than the ones it isn't. I compare the two halves because with only about 35 test rows a fixed cutoff like 0.80 might leave me with five predictions to judge. 10 points is under 2 rows at 17 predictions per half, so this is the noisiest of my five criteria, and I picked a small gap because I need it to hold on all three seeds.

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
