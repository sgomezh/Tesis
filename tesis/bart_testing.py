from ctypes.wintypes import WIN32_FIND_DATAA
from bartpy.sklearnmodel import SklearnModel
import numpy as np
import testing.dowhy_dataset as dataset
model = SklearnModel() # Use default parameters
X_training, Y_training = dataset.obtener_dataset()
print("X training: ", X_training)
print("Y training: ", Y_training[0])
model.fit(X_training, Y_training[0]) # Fit the model
predictions = model.predict(X_training) # Make predictions on the train set
X_testing, Y_testing = dataset.obtener_dataset()
out_of_sample_predictions = model.predict(X_testing) # Make predictions on new data