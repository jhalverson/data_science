# Jonathan Halverson
# Monday, January 18, 2016

# This script illustrates some basic features of the R
# environment. It is based on a tutorial from OpenIntro Statistics.

# load the data which gives health, age, smoking, weight, etc.
cdc = read.csv("data_science/statistics/cdc.csv")

# print out the first and last few lines
head(cdc)
tail(cdc)
tail(cdc, 10)

# find out the names of the columns
names(cdc)

# the dimensions of the data frame
dim(cdc)

# univariate descriptive statistics of a column
summary(cdc$weight)
boxplot(cdc$weight)
mean(cdc$weight)
var(cdc$weight)
max(cdc$weight)
sd(cdc$weight)

# make contingency tables (good for categorical data)
cases <- dim(cdc)[1]
table(cdc$smoke100) / cases
table(cdc$genhlth) / cases

# let's look at smoking
barplot(table(cdc$smoke100))
smoke <- table(cdc$smoke100)
table(cdc$smoke100, cdc$gender) / cases
mosaicplot(table(cdc$gender, cdc$smoke100))

# the proportion of smokers by gender
mosaicplot(table(cdc$smoke100, cdc$gender) / cases)

# slicing (analogous to Python)
cdc[567,6]
cdc[1:10,6]
cdc[1:100,6]
cdc[1:100,5:6]
cdc[1:10,4:6]
cdc[1:10,]

# create a sequence
y <- 1:10
y
y[y < 5]

# create a function
squares <- function(x) {
  return(x^2)
}
squares(3)
squares(c(-1, 1, 3))
squares(1:5)

large_squares <- function(x, cutoff) {
  tmp = subset(x, x > cutoff)
  return(tmp^2)
}
large_squares(1:5, 3)

# create subsets to work with certain data
mdata <- subset(cdc, gender == "m")
pdata <- subset(cdc, gender == "m" & age > 30)
head(mdata)
head(pdata)

# use this for help or use the window in the lower right
?subset

h = subset(cdc, genhlth == "good" | genhlth == "very good" | genhlth =="excellent")
table(h$gender) / dim(h)[1]

# boxplots of height data for different genders
boxplot(cdc$height ~ cdc$gender)

# boxplot of weight minus desired weight
boxplot(cdc$weight - cdc$wtdesire ~ cdc$gender)

# here we check if body mass index is a predictor of health
# 703 is a conversion factor from lbs and inches to kilograms and meters
# Wikipedia says "Commonly accepted BMI ranges are underweight: under 18.5,
# normal weight: 18.5 to 25, overweight: 25 to 30, obese: over 30."
bmi <- (cdc$weight / cdc$height^2) * 703
boxplot(bmi ~ cdc$genhlth)
hist(bmi, breaks=40)

# these two figures show that much of the population is overweight or obese
# let's compute the percentage of cases with bmi > 25
fat <- bmi[bmi > 25.0]
100 * length(fat) / dim(cdc)[1] # 55.5%

# points below the line are people who want to lose weight while
# those above it want to gain weight
plot(cdc$weight, cdc$wtdesire, xlim=c(0, 600), ylim=c(0, 400), xlab="Weight", ylab="Desired Weight")
lines(1:800, 1:800)

wdiff <- cdc$weight - cdc$wtdesire
length(wdiff[wdiff > 0]) / cases # 63.8% want to lose weight
length(wdiff[wdiff == 0]) / cases # 28.1% are at their target
length(wdiff[wdiff < 0]) / cases # 8.1% want to gain weight
