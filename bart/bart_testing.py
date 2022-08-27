from ctypes.wintypes import WIN32_FIND_DATAA
from bartpy.sklearnmodel import SklearnModel
import numpy as np
import sys
import testing.dowhy_dataset as dataset
model = SklearnModel() # Use default parameters
X_training, Y_training, X_testing, Y_testing = dataset.obtener_dataset()
model.fit(X_training, Y_training) # Fit the model
predictions = model.predict(X_training) # Make predictions on the train set
out_of_sample_predictions = model.predict(X_testing) # Make predictions on new data