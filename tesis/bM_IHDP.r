options(java.parameters = "-Xmx1500m")
library(bartMachine)
library(caTools)
library(dplyr)

# Load data
data_adress <- "https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv"

dataset <- read.csv(url(data_adress), header = FALSE)
col_names <- list("t", "y_factual", "y_cfactual", "mu0", "mu1")

for (i in 1 : 25){
    col_names <- c(col_names, paste0('x', i))
}

names(dataset) <- c(col_names) # Renombramos las columnas

# Guardamos y removemos los datos contrafacticos
y_cfactual <- dataset$y_cfactual
head(dataset)
dataset <- dataset[, -3:-5]

# Empujar yfactual al final del dataset
dataset <- dataset[, c(1, 3:ncol(dataset), 2)]

dataset$t <- as.logical(as.integer(dataset$t))

# Division del dataset en train y test
split <- sample.split(dataset$y_factual, SplitRatio = 0.7)
train <- subset(dataset, split == TRUE)
test <- subset(dataset, split == FALSE)

# Duplicamos el dataset de prueba para poder hacer la prediccion contrafactual
test_cfactual <- data.frame(test)

for (treatment in test_cfactual$t){
    # Intercambiamos el tratamiento
    test_cfactual$t <- ifelse(test_cfactual$t == TRUE, FALSE, TRUE)
}

# Construccion y entrenamiento del modelo
bart_machine <- build_bart_machine(train[, 1:28], train[, 29], num_trees = 200)

# Prediccion de los datos facticos y contrafacticos
pred_factual <- predict(bart_machine, test[, 1:28])
pred_cfactual <- predict(bart_machine, test_cfactual[, 1:28])

# Calculo de la RMSE
rmse_factual <- sqrt(mean((pred_factual - test$y_factual)^2))

