library(bartMachine)
library(rlang)
library(caTools)
library(dplyr)
library(tidytreatment)

dataPath <- "D:\\Escritorio\\Codigo\\Tesis\\datasets\\jobs.csv"
data <- read.csv(dataPath, header = TRUE)

data$treatment <- as.logical(data$treatment)

unique(data$treatment)
# Split data
split <- sample.split(data$re78, SplitRatio = 0.8)
train <- subset(data, split == TRUE)
test <- subset(data, split == FALSE)

bart = build_bart_machine(train[, -which(names(train) == 're78')], train$re78, num_trees = 200)
#bart = bartMachineCV(train[, -which(names(train) == 'y_factual')], train$y_factual)

ate = avg_treatment_effects(bart, "treatment")

print(ate[1,])
print(ate[1000, ])

mean(ate$ate)

head(ate)