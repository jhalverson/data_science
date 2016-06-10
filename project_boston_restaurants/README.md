#Keep It Fresh: Predict Restaurant Inspections

###Jonathan Halverson

####Introduction

The purpose of this contest was to develop a model to predict hygiene violations for 1851 restaurants in Boston. Contestants were given publicly available past violation data as well as Yelp data (reviews, tips, business info, check-ins, user info). This was a real competition used by the City of Boston to identify restaurants that should receive greater scrutiny. My two-person team Glouston finished 12th out of 525.

####Exploratory data analysis

The data consisted of several files in JSON or CSV format.
There were numerous duplicate inspection results. We removed duplicates that were
separated by fewer than 60 days.

We began by ignoring the Yelp data and [investigating the violation data](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_1_no_yelp.ipynb). For each inspection
the number of 1-, 2- and 3-star violations is given along with the date.
Most restaurants are inspected about 1-4 times per year.
Inspections were carried out Monday through Friday and a few on Sunday
but almost none on Saturday. There are about 2500 inspections per year.
However, in 2012 there were more than 3500.

It is difficult to estimate the size of the restaurant. One would think that
the bigger the kitchen the more violations there would be. We examined
the Yelp check-in data but found [no correlation](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_3_checkins.ipynb) between the number
of check-ins and the number of violations.

We found a modest correlation between the number of violations and the number of inspections (r = 0.39, p = 0.0). One might think that expensive restaurants have cleaner kitchens but this was not found. To check
for correlation throughout this work we computed the Pearson and Spearman correlation coefficients along with their
corresponding p-values.

The Yelp business data was used to get a sense of the effect of [neighborhood and categories](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_2_yelp_business_data.ipynb).
Dudley Square, Fields Corner and Chinatown were found to be the worst neighborhoods for
clean kitchens while Fenway, Back Bay and Hyde Park had the fewest violations on average.
For food categories, of the restaurants with more than 1 inspection, the most violations were
Dominican, Dim Sum, Tapas, Vietnamese and Chinese whereas those with the fewest were
Tobacco Shops, Gay Bars, Cheesesteaks and Moroccan.
Analyzing additional attributes such as BYOB, Delivery, Take-out, Wheelchair accessible did not
reveal much.

Seasonality in the number of inspections was examined by computing the correlation between the mean temperature averaged over a week and the number of [inspections per week](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_2b_correlation_time.ipynb). A moderate correlation was found (r = -0.41, p = 0.002) which could be explained by inspectors going on vacation during the summer months.

We also computed the [autocorrelation function](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_2b_correlation_time.ipynb) of the number of violations over all restaurants. On the time scale of 1-2 weeks the function was found to decrease as expected. However, around the 3-week mark it becomes negative and remains so until around week 13 when it becomes zero. One may reason that when a restaurant is inspected and the resulting number of violations is above the average, the restaurant tends to have fewer violations when re-inspected between 3 and 12 weeks later. Likewise, when the number of violations is small, maybe the restaurant gets careless and they have more violations during the 3 to 12 period after the inspection.

Each restaurant has an average star rating between 1 (worst) and 5 (best).
If the food or experience was not very good then the reviewer would choose
a low star value and then write text to explain why.
Early in the process we constructed a plot of average
star rating versus average number of violations and no correlation was found between
the two. This result suggests that only little predictive power lies in the text.

One factor that was thought to influence the number of violations was the nature of the
restaurant's neighborhood. To quantify good and bad neighborhoods we determined
the number of [crimes committed](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_2_yelp_business_data.ipynb) within a few blocks of each restaurant. This was referred
to as the crime density. The cutoff radius was taken as
1/20 the distance between North and South Station. Since there were 268,056 crimes
we used a binning procedure to assign each crime to a cell in a 2-d grid. This allowed us to
consider only the crimes in the nearest-neighbor cells of the restaurant.
There was no correlation between number of violations and crime density.

The [user data](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_4_user_data.ipynb) gives us information about the people who wrote the reviews. We are given
their average star value, number of Yelp friends, number of reviews written,
date they joined Yelp and other attributes. We also have information about how the Yelp
community thought of each of their reviews. One could use this information to
weight certain users or reviews but we did not try this because the time information is not available. There is a correlation (r = 0.83)
between the number of useful votes received by a reviewer and the number of
fans they have.

Yelp tip data is very similar to the review data. A plot of date versus number of
characters per tip indicates that Yelp [changed their character limit twice](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_5_tip_data_exploration.ipynb). The average
number of characters in a tip is 56.8. We did not use the tip data in our models.

####Models

A range of models from simple to complex were considered:

* Model 0: Predict the median value of all the data for each of the violation levels for all restaurants. This corresponds to 3, 0, 0 for 1-, 2- and 3-star violations, respectively. A simple model like this is useful for benchmarking purposes.

* Model 1: Predict the median value for each restaurant using only the data specific to each restaurant for all time. This model was effective which emphasizes the importance of the inspection history data relative to the Yelp data.

* Model 2: Predict the median value for each restaurant using data specific to the restaurant up to
the inspection date. This model uses extrapolation, which ultimately is required for the contest.

* Model 3: Fit a line to the entire violation data of each restaurant and evaluate this equation for predictions.

* Model 4: Train a model by relating recent Yelp reviews to the violation data. A bag of words model
with TF-IDF was used on the Yelp reviews. Reviews written within a certain time window before the inspection were used.
We used BeautifulSoup to remove any HTML. Regualr expressions were used to
remove non-alphabetical characters like numbers and punctuation. We setup
a pipeline to optimize the model where stop words, stemming were considered.
The model used n-grams up to tri-grams. We found better results were obtained when all the reviews
within the window were combined instead of associating each individual review with the corresponding
violation score. Ridge regression was used.

* Model 5: From the exploratory data analysis we found that categories were telling. We constructed a [series of models](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_8_categories_neighborhoods_model.ipynb) by using one-hot encoding to prepare the features and Lasso regression as the model. This was also done for neighborhoods as well and the combination of the two.

####Results

Below is a table summarizing ours results. These result are based on a train-test split.

| Model | Mean square error (train) | Mean square error (train) |
|:---------:|:---------|:-----------:|
|0 | Generic median model (train) | 18.6  |
|0 | Generic median model (test) | 16.9  |
|1 | Specific mean model using all data (train) | 13.6  |
|1 | Specific mean model using all data (test) | 12.8  |
|1 | Specific mean model using data up to inspection (test) | 12.8  |
|1 | Specific mean model using data up to inspection (test) | 12.8  |
|2 | LinearRegression using all data (train) | |
|2 | LinearRegression using all data (test) | |
|3 | RandomForestRegression (train) | |
|3 | RandomForestRegression (test) | |

####Conclusions

The model proved to work fairly well judging by our leaderboard score of 12th of 525. It would have been nice to have Yelp data available right up to the day of the inspection or at least the week before but the contest was not run in this way. New hires, a change of distributor or construction projects can quickly alter the quality of service.
