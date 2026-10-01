# Operations Analytics Capstone — In Progress

This page is not a finished project. There is no new code here, and there is no Power BI file. The numbers below are the printed output of projects 1, 3, and 5. Each of those scripts builds its own sample. They are not one plant extract, so the percentages must not be read as a single study.

## Question

Which machine should maintenance look at first, and is the gap large enough to act on?

## What is done

Project 1, SQL, 30 days, 4 machines, 120 production rows (`random.seed(1)`):

| Machine | Units | Defects | Defect rate |
|---|---:|---:|---:|
| Welder D | 14,790 | 781 | 5.28% |
| Press B | 15,605 | 275 | 1.76% |
| Welder C | 15,590 | 271 | 1.74% |
| Press A | 15,040 | 238 | 1.58% |

Welder D is the only machine above the factory average defect rate. Its worst day in that sample is 2026-01-01, with 40 defects.

Project 3, EDA, 90 days, 4 machines, 3 shifts, 360 rows (`np.random.seed(2)`):

- Welder D average defect rate: **5.43%**. Press A is 1.96%, Press B 1.90%, Welder C 1.88%.
- Night shift defect rate: **3.62%**, against **2.34%** on the other shifts.
- Welder D by shift: Evening 5.00%, Morning 4.92%, Night 6.23%.
- Correlation of downtime and defect rate: **0.07**. Downtime does not explain the defects in this sample.

The three charts from that run are in `03_eda_operations/`.

Project 5, a separate 60-day sample for Welder C and Welder D only (`np.random.seed(4)`). These are daily defect counts, not the rates above.

- Welder C mean: **10.07** defects per day (95% CI 9.31 to 10.83).
- Welder D mean: **14.33** defects per day (95% CI 13.59 to 15.08). The intervals do not overlap.
- Two-sample t-test: **t = -8.015**, and the script prints **p-value = 0.0000**. The value is about 8.85e-13, so it is below 0.05. On this sample, the two machines do not have the same mean.
- Speed against defects: Pearson **r = 0.61**. That is association, not a cause.

## What is not done

Project 4 prepares `kpi_data.csv` and lists Power BI steps. There is no `.pbix` and no dashboard screenshot, so this capstone does not cite a dashboard.

The night-shift gap is from project 3. The t-test is from project 5. Project 5 does not test shifts, and it does not use the project 3 rows. A finished version has to run one shared sample through SQL, the cleaning step, the EDA, and the t-test, then paste those prints here.

## Recommendation, limited to these samples

On the SQL sample and the EDA sample, look at Welder D first. On the EDA sample, the night shift is higher on every machine, and it is highest on Welder D. On the statistics sample, Welder D's daily defect count is higher than Welder C's, and the difference is not noise in that draw. Do not treat the 5.28%, the 5.43%, and the 14.33 defects per day as three measurements of one week.
