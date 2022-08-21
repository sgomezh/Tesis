#--------------------- Librerías importadas ---------------------
# I. Create a causal model from the data and given graph.
from dowhy import CausalModel
import dowhy.datasets
import warnings
from sklearn.exceptions import DataConversionWarning
import sys
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
from IPython.display import Image, display
import numpy as np

def obtener_dataset():
    #--------------------- Configuraciones de Encoder ---------------------
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    #--------------------- Ignorar warnings ---------------------
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    warnings.filterwarnings(action='ignore', category=FutureWarning)
    #========================== PASO 1 ==========================
    # Crear un modelo causal desde un set de datos y un grafo dado 
    #=============================================================
    # Cargar una muestra del dataset creado
    # Value of the coefficient [BETA]
    BETA = 10
    # Number of Common Causes
    NUM_COMMON_CAUSES = 2
    # Number of Instruments
    NUM_INSTRUMENTS = 1
    # Number of Samples
    NUM_SAMPLES = 100000
    # Treatment is Binary
    TREATMENT_IS_BINARY = False
    data = dowhy.datasets.linear_dataset(
        beta=10,
        num_common_causes=5,
        num_instruments=4,
        num_samples=10000,
        treatment_is_binary=True)
        
    '''     "df": data,
            "treatment_name": treatments,
            "outcome_name": outcome,
            "common_causes_names": common_causes,
            "instrument_names": instruments,
            "effect_modifier_names": effect_modifiers,
            "frontdoor_variables_names": frontdoor_variables,
            "dot_graph": dot_graph,
            "gml_graph": gml_graph,
            "ate": ate  
    '''
    dataset = data['df']  
    dataset_dict = {}
    X= np.array([])
    Y= np.array([])
    columns = dataset.columns.values
    for i in range(len(columns)):
        name = columns[i]
        value = dataset[name]
        dataset_dict[name] = list(value)
        if name != "y":
            print("X: ")
            print(name)
            if name == "v0":
                list_value=list(value)
                v0value = []
                for j in range(len(list_value)):
                    
                    if list_value[j] == True:
                        v0value.append(1.0)
                    if list_value[j] == False:
                        v0value.append(0.0)
                    dataset_dict[name] = list(v0value)
            X= np.append(X, dataset_dict[name])
            print(dataset_dict[name])
            
        if name == "y":
            print("Y: ")
            print(name)
            Y= np.append(Y, dataset_dict[name])
            print(dataset_dict[name])
    split = int(NUM_SAMPLES/2)
    end = int(len(dataset_dict))
    X_training = matrix[0:split]
    Y_training = matrix[0:split]
    X_testing = matrix[0:split]
    Y_testing = matrix[0:split]
                                
