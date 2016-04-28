# Predict Blood Donations
### Hosted by DrivenData.org

The objective is to predict a donation in March 2007.

** Exploratory data analysis **

We are given four features for 576 samples. However, two of the columns are
perfectly correlated. Several plots were made.

### Feature engineering

The average time between donations and others.

* Model training and cross validation

Six total featurs were considered. All possible combinations of features
were constructed using the itertools Python module. This extra loop is
computationally expensive for some models but it helps with refinement.

GridSearchCV with 10 folds of stratified cross validation were performed
for each set of hyperparameters. The log loss scoring was computed for
each case and each set of features.

Bagged Logistic Regression
1. 'months_since_last', 'number_of_donations', 'months_since_first', 'months_btwn_donation', 'inverse_first'
2. 'months_since_last', 'number_of_donations', 'months_since_first', 'last_to_first', 'months_btwn_donation', 'inverse_first'
3. 'months_since_last', 'number_of_donations', 'months_since_first', 'last_to_first'


For RandomForest it was necessary to set min_samples_leaf to a value much greater than
1 because otherwise it predicts 0 or 1 for certain cases which leads to large
penalties with log loss scoring.

* Results

We obtained our best leaderboard score using logistic regression
with features:.

* Conclusions


|model                      | leaderboard score|
|:--------------------------|:-----------------:|
|LogisticRegression       |            0.4370|
|AdaptiveBoosting             |            0.4809|
|KNearestNeighbors |            0.4370|
|RandomForest|            0.4370|
|GradientBoosting|            0.4370|
|SVM|            0.4370|

