# Optional review of the scores

The charts in `reports/figures` are the review page.

- `class_balance.png` shows that failures are uncommon.
- `recall_comparison.png` shows that the baseline catches none of them.
- `confusion_matrix.png` shows missed failures in the bottom-left cell and false alarms in the top-right cell.

`data/processed/coefficients.csv` is there if you want to sort the features in Excel. Hours since maintenance is the largest coefficient in the published sample. Pressure is smaller and was not used to create the label.
