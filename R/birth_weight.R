# Jonathan Halverson
# Monday, March 16, 2016

# Here determine if smoking affects birth weight

# download the raw data
setwd("data_science/R")
nc = read.csv("../statistics/nc.csv")

summary(nc)
by(nc$weight, nc$habit, mean)
inference(y = nc$weight, x = nc$habit, est = "mean", type = "ht", null = 0,
          alternative = "twosided", method = "theoretical")
inference(y = nc$weight, x = nc$habit, est = "mean", type = "ci", null = 0, 
          alternative = "twosided", method = "theoretical", 
          order = c("smoker","nonsmoker"))