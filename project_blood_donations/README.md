# Predict Blood Donations: DrivenData.org Competitiion
### Jonathan Halverson

#### Overview

Data is given by 576 blood donation volunteers. We are given their id number, number of months since
their first donations, number of months since their last donation, total number of donations, total
volume of blood donated and whether or not they donated in March 2007. The goal of the contest
to create a model that predicts the probability of a given volunteer in the test set donating blood
in March 2007. Scores are determined by the log loss metric.

Read about the [competition](https://www.drivendata.org/competitions/2/page/5/).
Check my score for jhalverson on the [leaderboard](https://www.drivendata.org/competitions/2/leaderboard/).

#### Exploratory data analysis

I began the problem by exploring the data ([see notebook](https://github.com/jhalverson/data_science/blob/master/project_blood_donations/exploratory_data_analysis.ipynb)). The correlation matrix showed that two features were perfectly correlated so one of them was dropped. Several plots were then constructed
of the remaing three features.

#### Feature engineering

Feature engineering usually determines the success of the model. I created three new features: average number of months between donations, the ratio of the number of months sinces the first donation to that of the last, and the inverse of months since first.

The Python itertools module was used to generate a list of different combinations of features. For each model we considered all combinations of the six features (three given plus three derived) from triples up to the full set. For each model and each feature set, the model's hyperparameters were optimzed using stratified K-fold cross validation. An attempt was made use nested cross validation but it proved to be computationally infeasible.

#### Results

Several models were attempted. For RandomForest it was necessary to set min_samples_leaf to a value much greater than
1 because otherwise it predicts 0 or 1 for certain cases which leads to large
penalties with log loss scoring.

|model                      | leaderboard score|
|:--------------------------|:-----------------:|
|BaggedLogisticRegression       |            0.4360|
|LogisticRegression       |            0.4370|
|MajorityVotingEnsemble | 0.4438|
|KNearestNeighbors |            0.4474|
|RandomForest|            0.4521|
|SVC/RBF|            0.4590|
|GradientBoosting|            0.4634|
|AdaptiveBoosting             |            0.4809|
|SVC/Linear|            0.4905|

#### Conclusions

Our best result was obtained using bagging with logistic regression as the base estimator. Each model was optimized for each feature set. It may be possible to improve on the result by using neural networks.
