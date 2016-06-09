# Keep It Fresh: Predict Restaurant Inspections

###Jonathan Halverson

####Introduction

We are given hygiene inspection voliation data for 1851 restaurants in Boston. The data begin in 2007. The goal is to combine Yelp review to predict future violations. This was a real competition used by the City of Boston to target potential violators.

#### Data cleaning

There were numerous duplicate inspections. We removed duplicates that were
separated by fewer than 60 days.

####Exploratory data analysis

We began by ignoring the Yelp data and investigating the violation data. For each inspection
there are a reported number of 1-, 2- and 3-star violations.
Most restaurants are inspected about 4-5 times per year.
Inspections were carried out Monday through Friday and a few on Sunday
but almost none on Saturday. There are about 2500 inspection per year.
However, in 2012 there were more than 3500.

It is difficult to estimate the size of the restaurant. One would think that
the bigger the kitchen the more violations there would be. We examined
the Yelp check-in data but found no correlation between the number
of check-ins and the number of violations.

We found a correlation between the number of violations and the number of inspections (r = 0.39). There
is no correlation between number of violations and the price range of the restaurant. One might
think that expensive restaurants have cleaner kitchens but this was not found. To check
for correlation we computed the Pearson and Spearman correlation coefficients along with their
corresponding p-values.

The Yelp business data was used to get a sense of the effect of neighborhood and categories.
Dudley Square, Fields Corner and Chinatown were found to be worst neighborhoods for
clean kitchens while Fenway, Back Bay and Hyde Park had the fewest violations on average.
For food categories, the restaurants with more than 1 inspection that had the most violations were
Dominican, Dim Sum, Tapas, Vietnamese, Chinese whereas those with fewest were
Tobacco Shops, Gay Bars, Cheesesteaks and Moroccan.
Additional attributes such as BYOB, Delivery, Take-out, Wheelchair accessible do not
reveal much.

Each restaurant has an average star rating between 1 (worst) and 5 (best).
Our initial thinking was that the Yelp star rating would give great insight into predicting
the number of violations. We thought that it would allow us to not deal with the text of the
review. To be clear, if the food or experience was not very good then the reviewer would give
the review a low star value and then write text to explain why.
However, early in the process we constructed a plot of average
star rating versus average number of violations and no correlation was found between
the two. At this point we had already invested a fair amount of time in a bag of words
based model which was not performing very well. So this plot explained our mixed results.

One factor that was thought to influence the number of violations was the nature of the
neighborhood the restaurant was in. To quantify good and bad neighborhoods we determined
the number of crimes committed within a few blocks of each restaurant. This was referred
to a the crime density. The cutoff radius was taken as
1/20 the distance between North and South Station. Since there were 268,056 crimes
we used a binning procedure to assign each crime to a 2-d grid. This required us to
consider only the crimes in the 9 bins around the restaurant.
There was no correlation between number of violations and crime density.

The user data gives us information about the people who wrote the reviews. We are given
their average star value, number of Yelp friends, number of reviews written,
date they joined Yelp and other attributes. We also have information about how the Yelp
community thought about each of their reviews. One could use this information to
weight certain users or reviews but we did not try this. There is a correlation (r = 0.83)
between the number of useful votes received by a reviewer and the number of
fans they have.

Yelp tip data is very similar to the review data. A plot of date versus number of
characters per tip indicates that Yelp change their character limit twice. The average
numbers of characters in a tip is 56.8. We did not use the tip data in our models.

####Feature extraction and engineering

One model is based on using the user reviews. The idea was to only consider
the reviews written in the days leading up to the inspection.

We used BeautifulSoup to remove any HTML. Regualr expressions were used to
remove non-alphabetical characters like numbers and puncuation. We setup
a pipeline to optimize the model. We considered cases where the reviews
where all combined and kept individually. A Porter stemmer was considered
as well as the removal of stop words. TF-IDF was used as well as
n-grams up to trigrams. 

We used the one-hot encoding to make features based on both neighborhood
and categories.

####Models

We began by thinking of simple models that did not use the Yelp data. This was done to produce simple benchmarks that are easily understood. This approach allows one to ensure that progress is made as the model is made more complex.

Our first attempt to use the Yelp data considered only the star ratings.

The simplest model is to predict the median value for each of the violation levels for all restaurants. This corresponds to 3, 0, 0. The next more complicated model would be to predict the median value for each restaurant. 

Our approach was to association reviews with violations over a given date range. For instance, to predict violations at
a given restaurant on a given date, the code would consider.

####Unresolved issues

Are the duplicates a problem. What about null values? Could more be done with the other data.

#### Results

| Model | Mean Square Error |
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

The model proved to work fairly well judging by our leaderboard score. It would have been nice to use the Yelp data right up to the day of the inspection or at least the week before. New hires, a change of distributor or construction projects can quickly alter the quality of service.
