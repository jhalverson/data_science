# Predict Blood Donations: DrivenData.org Competitiion
### Jonathan Halverson

#### Introduction

This document describes my solution to the Predict Blood Donations machine learning competition
hosted by DrivenData.org. The goal of the contest is
to create a model that predicts the probability of a given volunteer in the test set to donate blood
in March 2007. The training data consists of 576 blood donation volunteer records. For each
volunteer we are given their id number, number of months since
their first donations, number of months since their last donation, total number of donations, total
volume of blood donated and whether or not they donated in March 2007. Scores are determined by the log loss metric.

Read about the [competition](https://www.drivendata.org/competitions/2/page/5/) or check my score (jhalverson) on the [leaderboard](https://www.drivendata.org/competitions/2/leaderboard/).

#### Exploratory data analysis

I began the problem by exploring the data ([see notebook](https://github.com/jhalverson/data_science/blob/master/project_blood_donations/exploratory_data_analysis.ipynb)). The correlation matrix of features showed that two features (total volume and number of donations) were perfectly correlated so one of them was dropped. Several plots were then constructed of the remaing three features including a three-dimensional scatter plot. After inspecting the various figures it was not obvious how to distinguish between the two classes.

#### Feature engineering

Feature engineering is usually crucial for a successful model. I created three new features: average number of months between donations, the ratio of the number of months since the last donation to that of the first, and the inverse of months since first.

The Python itertools module was used to generate a list of different combinations of features. For each model we considered all combinations of the six features (three given plus three derived) from triples up to the full set. For each model and each feature set, the hyperparameters of the model were optimzed using stratified K-fold cross validation. To reduce the generalization error, an attempt was made use nested cross validation but it proved to be computationally infeasible.

#### Results

It is always wise to try several models since each has strengths and weaknesses. For random forest it was necessary to set minimum samples per leaf parameter to a value much greater than 1 (e.g., 20-40) because otherwise it predicts 0 or 1 for certain cases which leads to large penalties with log loss scoring. Similarly, for KNN a large number of neighbors proved to be optimum (e.g., 30-50). The support
vector machine model took the longest to optimize (12 hours on 4-core laptop) and our grid was chosen to be sparse to aid this. For the majority voting classifier, we used bagged logistic regression, random forest and K-nearest neighbors. Due to the expense of optimizing this model we were only able to consider a sparse grid of hyperparameters. This explains why it did not do the best of all the models.

The table below gives the score found for each optimized model:

|Model                      | Leaderboard Score|
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

Our best result was obtained using bagging with logistic regression as the base estimator. In general this is a fairly noisy data set. One must be very careful to avoid overfitting. This was accomplished using stratified K-fold cross validation with shuffling. Our model performs very well. Other contestants have reported success with using neural networks.
