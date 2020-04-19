library(class)

# choose Session from menu then Set Working Directory
setwd("~/rc/workshops/spring_2020/machine_learning/R/chapter3_knn")

df_raw <- read.csv("wisc_bc_data.csv", stringsAsFactors = FALSE, header = TRUE)
df_raw <- df_raw[-1]  # remove first column of ids

table(df_raw$diagnosis)
prop.table(table(df_raw$diagnosis))

summary(df_raw[c("diagnosis", "radius_mean")])

minmax <- function(x) {
  return ((x - min(x)) / (max(x) - min(x)))
}

df_raw$diagnosis <- factor(df_raw$diagnosis)  # could also set levels and labels
#df_raw[1] <- factor(df_raw[1]) # did not work

str(df_raw)

plot(df_raw$radius_mean, df_raw$texture_mean)
cor(df_raw$radius_mean, df_raw$texture_mean)
boxplot(df_raw$radius_mean)
hist(df_raw$radius_mean)

df_n <- as.data.frame(lapply(df_raw[2:31], minmax))

summary(df_n)

X_train <- df_n[1:469,1:30]
y_train <- df_raw[1:469,1]
X_test <- df_n[470:569,1:30]
y_test <- df_raw[470:569,1]

pred <- knn(X_train, X_test, cl=y_train, k=21)

table(pred)

library(gmodels)

CrossTable(y_test, pred)
