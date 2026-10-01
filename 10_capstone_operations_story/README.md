# Project 10, the capstone, one operations story

This project has no new code. It puts projects 1 to 5 together into one story a plant manager could follow, which is how a real analyst delivers work.

## The story in one sentence

Welder D has the highest defect rate, it is worst on the night shift, the difference is statistically real and not noise, and here is the dashboard to keep track of it.

## The steps

First, SQL from project 1, pull the total units and defects per machine and find the worst one.

Second, pandas from projects 2 and 3, clean the export, group by machine and shift, and make the charts.

Third, statistics from project 5, a t-test to prove the worst machine really is different.

Fourth, Power BI from project 4, put the KPIs on a dashboard with slicers.

Fifth, write the one page summary below with a recommendation.

## The one page summary I fill in

Question, which machine should maintenance look at first?

Data, 90 days, 4 machines, 3 shifts.

Finding 1, Welder D defect rate is ___ percent against a factory average of ___ percent.

Finding 2, the night shift defect rate is ___ percent against ___ percent on the other shifts.

Statistical check, a two sample t-test with p equal to ___, below 0.05 means the difference is real.

Recommendation, inspect Welder D first and review the night shift procedure.

Dashboard, the screenshot from project 4.

## Why this project matters

Recruiters do not want ten separate scripts. They want to see that I can go from a business question, to the data, to a clear recommendation. That is what this project shows.
