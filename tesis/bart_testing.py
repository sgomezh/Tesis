from bartpy.sklearnmodel import SklearnModel
import numpy as np
import testing.dowhy_dataset as dataset
def bart():
    model = SklearnModel(n_trees= 150,
                    n_chains = 4,
                    sigma_a= 0.001,
                    sigma_b = 0.001,
                    n_samples= 50,
                    n_burn= 50,
                    thin= 0.1,
                    alpha= 0.95,
                    beta = 2.,
                    store_in_sample_predictions=True,
                    store_acceptance_trace=True,
                    n_jobs= 3) # Use default parameters

    X_training, Y_training, ate = dataset.obtener_dataset()
    '''print("X training: ", X_training)
    print("Y training: ", Y_training[0])'''
    print("fit")

    model.fit(X_training, Y_training[0]) # Fit the model

    print("Predict")

    predictions = model.predict(X_training) # Make predictions on the train set
    '''X_testing, Y_testing, ate = dataset.obtener_dataset()'''
    X0_testing, Y0_testing, X1_testing, Y1_testing, ate_dowhy= dataset.duplicar_dataset()
    '''out_of_sample_predictions = model.predict(X_testing) # Make predictions on new data'''
    y0 = model.predict(X0_testing)
    y1 = model.predict(X1_testing)
    print("ATE: ", calculateATE(y1, y0))
    print("ATE dowhy: ", ate_dowhy)

    '''print("out_of_sample_predictions: ", out_of_sample_predictions)
    print("Y_testing: ", Y_testing)'''



def calculateATE(y0: np.array, y1: np.array) -> float:
    """Calcula el efecto de tratamiento promedio"""
    if y0.shape != y1.shape:
        raise ValueError("y0 and y1 must have the same shape")

    return np.mean(y1 - y0)

if __name__ == "__main__":
    bart()