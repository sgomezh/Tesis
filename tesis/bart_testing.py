from ctypes.wintypes import WIN32_FIND_DATAA
from bartpy.sklearnmodel import SklearnModel
import numpy as np
import testing.dowhy_dataset as dataset
model = SklearnModel(n_trees = 100,
                 n_chains= 2,
                 sigma_a= 0.001,
                 sigma_b= 0.001,
                 n_samples = 20,
                 n_burn = 20,
                 thin= 0.1,
                 alpha = 0.95,
                 beta = 2.,
                 store_in_sample_predictions=True,
                 store_acceptance_trace=True,
                 n_jobs=1) # Use default parameters
X_training, Y_training = dataset.obtener_dataset()
'''print("X training: ", X_training)
print("Y training: ", Y_training[0])'''
model.fit(X_training, Y_training[0]) # Fit the model
predictions = model.predict(X_training) # Make predictions on the train set
print("--------------------------------------------------------------------------")
print("predictions: ", predictions)
print("lenn predictions: ", len(predictions))
X_testing, Y_testing = dataset.obtener_dataset()
out_of_sample_predictions = model.predict(X_testing) # Make predictions on new data
print("--------------------------------------------------------------------------")
print("out_of_sample_predictions: ", out_of_sample_predictions)
print("len out_of_sample_predictions: ", len(out_of_sample_predictions))





