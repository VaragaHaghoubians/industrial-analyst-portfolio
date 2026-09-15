# Project 2, cleaning messy data with pandas

Real factory exports are never clean. So for this project I first create a messy file on purpose, that way anyone can run it, and then I clean it one problem at a time and show the before and after.

## How to run it

```
python clean_data.py
```

It writes messy_production.csv, which is the problem, and clean_production.csv, which is the fix.

## The problems in the file and how I fixed them

Duplicate rows, I removed them with drop_duplicates().

The same machine written as "Press A", "press a" and " Welder C " with extra spaces, I fixed with str.strip() and str.title().

Numbers stored as text like "  520 " or even "unknown", I used pd.to_numeric with errors="coerce", so the bad ones become NaN instead of crashing the script.

A temperature of 999, which is a sensor error, anything above 150 becomes NaN.

Missing numbers, I fill them with the median, because the median is safer than the mean when there are outliers.

Missing shift, I label it "Unknown" rather than inventing a shift.

## Things I learned doing this

Always print isna().sum(), duplicated().sum() and unique() before and after. That is my proof the cleaning actually worked.

errors="coerce" is the trick for a column where a few values are text, the bad ones become NaN and everything else stays a number.

I fill with the median and not the mean, because one 999 would pull the mean way off.

