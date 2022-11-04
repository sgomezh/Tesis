library(bartMachine)
library(rlang)
library(caTools)
library(dplyr)
library(tidytreatment)

dataURL <- "https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv"
data <- read.csv(dataURL, header = FALSE)
# Create list of names
nList <- c("treatment", "y_factual", "y_cfactual", "mu0", "mu1")
for (i in 1:25) {
  nList <- c(nList, paste0("x", i))
}

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