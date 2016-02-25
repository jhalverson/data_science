# Jonathan Halverson
# January 12, 2016

# Here we analyze basketball data of one player during a few playoff games
# to determine if the hot hand phenomenon is real. If the effect is real we
# expect the make probability to increase after a made shot giving strings
# of consecutively made shots. We of course compare this with the result of
# chance alone where the make percentage is a constant for all shots.

# read file and get a sense of the data
kobe = read.csv("data_science/statistics/kobe.csv")
head(kobe)
dim(kobe)
attempts <- dim(kobe)[1]

# these two lines of course do the same thing
kobe[1:10,6]
kobe$basket[1:10]

# let's compute Kobe's make percentage
kobe$basket[kobe$basket == "H"]
make_frac <- dim(subset(kobe, basket == "H"))[1] / attempts
print(make_frac)

# an alternative definitions
table(kobe$basket)[1] / length(kobe$basket)
table(kobe$basket)[1] / attempts

# return a vector the number of consecutively made shots
calc_streak <- function(x) {
  y <- rep(0,length(x))
  y[x == "H"] <- 1
  y <- c(0, y, 0)
  wz <- which(y == 0)
  streak <- diff(wz) - 1
  return(streak)
}

# compute streaks and plot barplot
kobe_streak <- calc_streak(kobe$basket)
barplot(table(kobe_streak))

# here we check the function by making sure hits is the same
hits <- sum(0:4 * table(kobe_streak))
print(hits) # yields 58 which is correct

# we to check the null hypothesis of independent shots making sure the composition is the same
outcomes <- c("H", "M")
p <- c(make_frac, 1.0 - make_frac)
indep <- sample(outcomes, size = attempts, replace = TRUE, prob = p)
while (table(indep)[1] != table(kobe$basket)[1]) {
  indep <- sample(outcomes, size = attempts, replace = TRUE, prob = p)
}

barplot(table(calc_streak(indep)))
barplot(table(kobe_streak))

# Conclusion: While the two data sets show a resemblance, more data is needed
# in order to determine if the hot hand phenomenon is real. The hot hand
# phenomenon is still an area of active research.
