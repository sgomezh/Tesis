data(automobile)
head(automobile)
library(bartMachine)

automobile <- na.omit(automobile)
x <- automobile[, 1:ncol(automobile) - 1]
y <- automobile[, ncol(automobile)]

bart_machine <- build_bart_machine(x, y)
summary(bart_machine)
#investigate_var_importance(bart_machine)