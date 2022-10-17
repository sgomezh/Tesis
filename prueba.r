library(bartMachine)
library(rlang)
library(caTools)
library(dplyr)

# Load data
dataUrl <- "https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv"

data <- read.csv(dataUrl, header = FALSE, sep = ",")

names <- c("treatment", "y_factual", "y_cfactual", "mu0", "mu1")

for (i in 1:25) {
  names <- c(names, paste0("x", i))
}

colnames(data) <- names
write.csv2(data, "ihdp.csv")
# Remove y_cfactual and mu
data <- data[, c(1, 2, 4:30)]

data <- data %>% relocate(y_factual, .after = x25)

# Split data
set.seed(123)
split <- sample.split(data$y_factual, SplitRatio = 0.8)
train <- subset(data, split == TRUE)
test <- subset(data, split == FALSE)


# Train model
bart <- build_bart_machine(train[, 1:ncol(train)-1], train$y_factual, num_trees = 200)

sumario <- capture.output(summary(bart))

print(sumario)


pred <- predict(bart, test[, 1:ncol(test)-1])

# Calculate r squared
r_squared <- function(y, y_hat) {
  1 - sum((y - y_hat)^2) / sum((y - mean(y))^2)
}

print(r_squared(test$y_factual, pred))
plot(pred, test$y_factual)