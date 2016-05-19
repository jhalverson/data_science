# Keep It Clean: Machine Learning Contest

###Jonathan Halverson

####Introduction

We are given hygiene inspection voliation data for 1851 restaurants in Boston. The data begin in 2007. The goal is to combine Yelp review to predict future violations. This was a real competition used by the City of Boston to target potential violators.

####Exploratory data analysis




####Feature extraction and engineering

####Models

We began by thinking of simple models that did not use the Yelp data. This was done to produce simple benchmarks that are easily understood. This approach allows one to ensure that progress is made as the model is made more complex.

Our first attempt to use the Yelp data considered only the star ratings.

The simplest model is to predict the median value for each of the violation levels for all restaurants. This corresponds to 3, 0, 0. The next more complicated model would be to predict the median value for each restaurant. 

Our approach was to association reviews with violations over a given date range. For instance, to predict violations at
a given restaurant on a given date, the code would consider.

####Unresolved issues

Are the duplicates a problem. What about null values? Could more be done with the other data.

####Conclusions

The model proved to work fairly well judging by our leaderboard score. It would have been nice to use the Yelp data right up to the day of the inspection or at least the week before. New hires, a change of distributor or construction projects can quickly alter the quality of service.
