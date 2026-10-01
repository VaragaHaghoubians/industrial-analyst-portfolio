# Project 9, predictive maintenance, will this machine fail?

Here I predict machine failure from sensor readings, temperature, speed, torque and tool wear. Failures are rare, so this project is really about why accuracy is misleading and why recall is what matters for maintenance.

I use scikit-learn, a train and test split with stratify, class_weight="balanced" for the class imbalance, a confusion matrix, precision and recall, and feature importance.

## How to run it

```
python predict_failure.py
```

By default it makes similar fake sensor data. To use the real public dataset, download AI4I 2020 from the UCI repository and save it in this folder as ai4i2020.csv, the script picks it up automatically.

## The lesson in the results, on the sample data with about a 6 percent failure rate

Random Forest gets 0.94 accuracy but its recall on failures is about 0.01, it misses almost every single failure.

Logistic Regression gets only 0.65 accuracy but its recall on failures is about 0.70, it catches most of them, with more false alarms.

Random Forest looks better on accuracy but is useless for maintenance, because it just predicts "no failure" for everything. For maintenance I would pick the model with high recall, since missing a real failure costs far more than a false alarm.

## Things I learned doing this

With rare events, 94 percent accuracy can mean the model learned nothing at all.

stratify=y keeps the same failure percentage in train and test.

class_weight="balanced" tells the model to pay extra attention to the rare class.

Read the confusion matrix, not just the accuracy number.

Tool wear and torque were the most important sensors, those are the ones that go on the live dashboard.

