# Jonathan Halverson
# Wednesday, March 2, 2016

# This script illustrates linear regression.

# load the data
getwd()
setwd("data_science/R")
data = read.csv("linear.dat", sep=" ", header=TRUE)

# plot the data
plot(data$x, data$y, xlab="x", ylab="y")

# to apply linear regression the following must be satisfied:
# 1. the relationship appears linear
# 2. the variance is a constant
# 3. the residuals are normally distributed
# 4. the data points are independent

regmodel <- lm(data$y ~ data$x, data=data)
summary(regmodel)

# the p-values are found to be O(1e-16) indicating that
# the slope and intercept are non-zero

# plot the least squares fit with the data
s = seq(0.0, 2.5, by = 0.1)
t = 2.3108 * s + 5.5250
lines(s, t, type="l")