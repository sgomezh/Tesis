from ctypes.wintypes import WIN32_FIND_DATAA
from bartpy.sklearnmodel import SklearnModel
import numpy as np
model = SklearnModel() # Use default parameters
Z0 = [1, 1, 1, 1, 1]
Z1 = [0.002609,0.704278, 0.199509, 0.757431, 0.461664]
W0 = [ -0.736965, -1.173873, -1.869825, -0.541932, -1.101587]
W1 = [-1.251120, 0.032109, -1.688500, -0.529491, -2.094344]
V0 = [1, 1, 1, 1, 1]
outcome = [5.650407, 4.014683, 0.235048, 6.945162, 5.104259]
X = np.array([Z0, Z1, W0, W1, V0])
Y = np.array(outcome)
model.fit(X, Y) # Fit the model
predictions = model.predict(X) # Make predictions on the train set
#out_of_sample_predictions = model.predict(X_test) # Make predictions 