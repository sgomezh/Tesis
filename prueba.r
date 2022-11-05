library(bartMachine)
library(rlang)
library(caTools)
library(dplyr)
library(tidytreatment)

dataURL <- "https://users.nber.org/~rdehejia/data/nsw_treated.txt"
data <- read.csv(dataURL, header = FALSE)

# Save dataframe as csv
write.csv(data, "nsw_treated.csv", row.names = FALSE)

# Assign names to data
names(data) <- nList

# Remove y_cfactual
data <- data %>% select(-y_cfactual)

names(data)

write.csv(data, "ihdp_npci_2.csv", row.names = FALSE)


# Split data
split <- sample.split(data$y_factual, SplitRatio = 0.8)
train <- subset(data, split == TRUE)
test <- subset(data, split == FALSE)

#bart = build_bart_machine(train[, -which(names(train) == 'y_factual')], train$y_factual, num_trees = 200)
bart = bartMachineCV(train[, -which(names(train) == 'y_factual')], train$y_factual)

ate = avg_treatment_effects(bart, "treatment")

print(ate[1,])
print(ate[1000, ])

mean(ate$ate)

head(ate)