#Keep It Fresh: Predict Restaurant Inspections

###Jonathan Halverson

####Introduction

We are given hygiene inspection data for 1851 restaurants in Boston. The data begin in 2007. The goal is to use the inspection data in combination with Yelp data to predict future violations. This was a real competition used by the City of Boston identify restaurants that should be given greater scrutiny.

#### Data cleaning

The data consisted of several files in JSON or CSV format.
There were numerous duplicate inspection results. We removed duplicates that were
separated by fewer than 60 days.

####Exploratory data analysis

We began by ignoring the Yelp data and investigating the violation data. For each inspection
the number of 1-, 2- and 3-star violations is given along with the date.
Most restaurants are inspected about 1-4 times per year.
Inspections were carried out Monday through Friday and a few on Sunday
but almost none on Saturday. There are about 2500 inspections per year.
However, in 2012 there were more than 3500.

It is difficult to estimate the size of the restaurant. One would think that
the bigger the kitchen the more violations there would be. We examined
the Yelp check-in data but found no correlation between the number
of check-ins and the number of violations.

We found a correlation between the number of violations and the number of inspections (r = 0.39, p = 0.0). One might think that expensive restaurants have cleaner kitchens but this was not found. To check
for correlation throughout this work we computed the Pearson and Spearman correlation coefficients along with their
corresponding p-values.

The Yelp business data was used to get a sense of the effect of neighborhood and categories.
Dudley Square, Fields Corner and Chinatown were found to be worst neighborhoods for
clean kitchens while Fenway, Back Bay and Hyde Park had the fewest violations on average.
For food categories, the restaurants with more than 1 inspection that had the most violations were
Dominican, Dim Sum, Tapas, Vietnamese and Chinese whereas those with the fewest were
Tobacco Shops, Gay Bars, Cheesesteaks and Moroccan.
Analyzing additional attributes such as BYOB, Delivery, Take-out, Wheelchair accessible did not
reveal much.

Seasonality in the number of inspections was examined by computing the correlation between the mean temperature averaged over a week and the number of inspections per week.A moderate correlation was found (r = -0.41, p = 0.002) which is most likely explained by inspectors going on vacation during the summer months.

We also computed the [autocorrelation function](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_2b_correlation_time.ipynb) of the number of violations averaged over all restaurants. On the time scale of 1-2 weeks the function was found to decrease as expected. However, around the 3 week mark it goes negative and remains so until around week 13 when it goes to zero. One may reason that when a restaurant is inspected and the resulting number of violations is above the average, the restaurant tends to have fewer violations when re-inspected between 3 and 12 weeks later. Likewise, when the number of violations is small, maybe the restaurant gets careless and they have more violations during the 3 to 12 period after the inspection.

Each restaurant has an average star rating between 1 (worst) and 5 (best).
If the food or experience was not very good then the reviewer would choose
a low star value and then write text to explain why.
Early in the process we constructed a plot of average
star rating versus average number of violations and no correlation was found between
the two. This result suggests that only little predictive power lies in the text.

One factor that was thought to influence the number of violations was the nature of the
restaurant's neighborhood. To quantify good and bad neighborhoods we determined
the number of crimes committed within a few blocks of each restaurant. This was referred
to as the crime density. The cutoff radius was taken as
1/20 the distance between North and South Station. Since there were 268,056 crimes
we used a binning procedure to assign each crime to a cell in a 2-d grid. This allowed us to
consider only the crimes in the nearest neighbor cells of the restaurant.
There was no correlation between number of violations and crime density.

The user data gives us information about the people who wrote the reviews. We are given
their average star value, number of Yelp friends, number of reviews written,
date they joined Yelp and other attributes. We also have information about how the Yelp
community thought of each of their reviews. One could use this information to
weight certain users or reviews but we did not try this because the time information is not available. There is a correlation (r = 0.83)
between the number of useful votes received by a reviewer and the number of
fans they have.

Yelp tip data is very similar to the review data. A plot of date versus number of
characters per tip indicates that Yelp changed their character limit twice. The average
number of characters in a tip is 56.8. We did not use the tip data in our models.

####Feature extraction and engineering

A bag of words model with TF-IDF was used on the Yelp reviews. Reviews written
within a time window before the inspection were used to generate features.

We used BeautifulSoup to remove any HTML. Regualr expressions were used to
remove non-alphabetical characters like numbers and puncuation. We setup
a pipeline to optimize the model. We considered cases where the reviews
where all combined and kept individually. A Porter stemmer was considered
as well as the removal of stop words. TF-IDF was used as well as
n-grams up to trigrams. 

We used the one-hot encoding to make features based on both [neighborhood
and categories](https://github.com/jhalverson/data_science/blob/master/project_boston_restaurants/part_8_categories_neighborhoods_model.ipynb).

####Models

We began with simple models for benchmarking purposes.
The simplest model is to predict the median value for each of the violation levels for all restaurants. This corresponds to 3, 0, 0. The next more complicated model would be to predict the median value for each restaurant. This leads to a large improvement.

It turns out that if one only uses the median value for each restaurant up to
the inspection date (instead of all the data) the result is not very good.

Another simple model is to fit a line to the violation data and interpolate the
number of violations for a given inspection date. This proves to not work very well.

From the exploratory data analysis we found that categories were telling. We constructed a series of models by using one-hot encoding and Lasso. This was also done
for neighborhoods and the combination of the two.

Our approach was to association reviews with violations over a given date range. For instance, to predict violations at
a given restaurant on a given date, the code would consider.

#### Results

Below is a table summarizing ours results.


| Model description | Mean Square Error |
|:---------|:-----------:|
|Null model (train) | 18.6  |
|Null model (test) | 16.9  |
|Mean model (train) | 13.6  |
|Mean model (test) | 12.8  | 
|LinearRegression (train) | |
|LinearRegression (test) | |
|RandomForestRegression (train) | |
|RandomForestRegression (test) | |

The Null model is to guess (3, 0, 0). The Mean model is to guess the mean values of the violations for each
restaurant. These are simple models for benchmarking purposes and neither of them use the Yelp data.

####Conclusions

The model proved to work fairly well judging by our leaderboard score of 12th of 525. It would have been nice to have Yelp data available right up to the day of the inspection or at least the week before but the contest was not run in this way. New hires, a change of distributor or construction projects can quickly alter the quality of service.
