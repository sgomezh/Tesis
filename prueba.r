library(bartMachine)
library(rlang)
library(caTools)
library(dplyr)
library(gridGraphics)

data(automobile)
automobile <- na.omit(automobile)

# Split data
split <- sample.split(automobile$log_price, SplitRatio = 0.8)
train <- subset(automobile, split == TRUE)
test <- subset(automobile, split == FALSE)

png(filename = "D:/Escritorio/Codigo/Tesis/Predicciones/varimp.png")

bart = build_bart_machine(train[, -which(names(train) == 'log_price')], train$log_price, num_trees = 200)

investigate_var_importance(bart)

dev.off()


# # Train model
# bart <- build_bart_machine(train[, 1:ncol(train)-1], train$log_price, num_trees = 200)

# sumario <- capture.output(summary(bart))

# print(sumario)

