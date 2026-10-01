# Start here

This project is about a rare failure label, not about building a complicated model.

1. Read the README. One row is one machine on one day.
2. Run `src/main.py` and write down three numbers: baseline accuracy, baseline recall, model recall.
3. Open the notebooks in number order.
4. Look at the confusion matrix and say which corner is a missed failure.
5. Answer the first four questions in `docs/interview_questions.md`.

## What each script does

| File | Simple explanation |
|---|---|
| src/generate_data.py | Builds 720 machine-days with seed 42 |
| src/cleaning.py | Checks the label and keeps the model inputs separate from it |
| src/model.py | Compares "always no failure" with balanced logistic regression |
| src/visualization.py | Draws class balance, recall and the confusion matrix |
| src/reporting.py | Writes the scores from that one test split |
| src/main.py | Runs these steps in order |

The model inputs are vibration, temperature, pressure and hours since maintenance. Failure is the label. It is not an input.

## Practice

Explain this sentence without looking at the chart: the baseline is more accurate and less useful.

Then say what precision of 25.6% means for a technician who has to walk to the machine.

## Honest presentation

The failure rule was written into the simulator, and the test split is random inside the same sample. Say what recall and precision mean. Do not say this model is ready for a factory.
