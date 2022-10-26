library(bartMachine)
library(rlang)
library(caTools)
library(dplyr)

# Load data
#dataUrl <- "https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv"

data(automobile)
automobile <- na.omit(automobile)

# Split data
set.seed(123)
split <- sample.split(automobile$log_price, SplitRatio = 0.8)
train <- subset(automobile, split == TRUE)
test <- subset(automobile, split == FALSE)


# Train model
bart <- build_bart_machine(train[, 1:ncol(train)-1], train$log_price, num_trees = 200)

sumario <- capture.output(summary(bart))

print(sumario)

