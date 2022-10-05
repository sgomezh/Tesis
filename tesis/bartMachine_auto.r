library("bartMachine")
library("caTools")

data(automobile)

head(automobile)

automobile <- na.omit(automobile)

colnames(automobile)

sample <- sample.split(automobile$log_price, SplitRatio = 0.7)
train <- subset(automobile, sample == TRUE)
test <- subset(automobile, sample == FALSE)

bart <- build_bart_machine(train[, 1:ncol(train)-1], train$log_price)

bart_predict_for_test_data(bart, test[, 1:ncol(test)-1], test$log_price)

investigate_var_importance(bart)

write.csv(automobile, "automobile.csv", row.names = FALSE)