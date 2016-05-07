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

Majority voiting
1. Optimal score: 0.47
Optimal features:  ['number_of_donations', 'months_since_first', 'last_to_first', 'months_btwn_donation']
Optimal parameters:  {'blr__base_estimator__C': 10.0, 'blr__n_estimators': 50, 'knn__n_neighbors': 20, 'rf__min_samples_leaf': 40}

2. Optimal score: 0.47
Optimal features:  ['number_of_donations', 'months_since_first', 'last_to_first', 'months_btwn_donation', 'inverse_first']
Optimal parameters:  {'blr__base_estimator__C': 1.0, 'blr__n_estimators': 100, 'knn__n_neighbors': 20, 'rf__min_samples_leaf': 20}

3. Optimal score: 0.47
Optimal features:  ['months_since_last', 'number_of_donations', 'months_since_first', 'last_to_first', 'months_btwn_donation']
Optimal parameters:  {'blr__base_estimator__C': 10.0, 'blr__n_estimators': 25, 'knn__n_neighbors': 20, 'rf__min_samples_leaf': 20}

----

Bagged Logistic Regression
1. 'months_since_last', 'number_of_donations', 'months_since_first', 'months_btwn_donation', 'inverse_first'
2. 'months_since_last', 'number_of_donations', 'months_since_first', 'last_to_first', 'months_btwn_donation', 'inverse_first'
3. 'months_since_last', 'number_of_donations', 'months_since_first', 'last_to_first'

SVC Linear
Optimal features:  ['months_since_last', 'number_of_donations', 'months_since_first', 'months_btwn_donation', 'inverse_first']
Optimal parameters:  {'kernel': 'linear', 'C': 1.0, 'shrinking': True}

SVC RBF
Optimal score: 0.48
Optimal features:  ['months_since_last', 'last_to_first', 'months_btwn_donation', 'inverse_first']
Optimal parameters:  {'kernel': 'rbf', 'C': 100.0, 'shrinking': False, 'gamma': 0.10000000000000001}


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
|SVCLinear|            0.4370|
|SVCRBF|            0.4370|

