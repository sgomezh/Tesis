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
    # Value of the coefficient [BETA] (real effect)
    BETA = 10
    # Number of Common Causes
    NUM_COMMON_CAUSES = 500
    # Number of Instruments
    NUM_INSTRUMENTS = 499
    # Number of Samples
    NUM_SAMPLES = 1000
    # Treatment is Binary
    TREATMENT_IS_BINARY = True
    data = dowhy.datasets.linear_dataset(
        beta=BETA,
        num_common_causes=NUM_COMMON_CAUSES,
        num_instruments=NUM_INSTRUMENTS,
        num_samples=NUM_SAMPLES,
        treatment_is_binary=TREATMENT_IS_BINARY)
        
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
    ate = data['ate']
    '''print("ATE: ", ate)  '''
    dataset_dict = {}
    X= []
    Y= []
    columns = dataset.columns.values
    for i in range(len(columns)):
        name = columns[i]
        value = dataset[name]
        dataset_dict[name] = list(value)
        if name != "y":
            '''print("X: ")
            print(name)'''
            if name == "v0":
                dataset_dict[name] = convert_to_binary(value)
            X.append(dataset_dict[name])
            '''print(dataset_dict[name])'''
            
        if name == "y":
            '''print("Y: ")
            print(name)'''
            Y.append(dataset_dict[name])
            '''print(dataset_dict[name])'''
    split = int(NUM_SAMPLES/2)
    end = int(len(dataset_dict))

    X = np.array(X)
    Y = np.array(Y)

    '''print("X: ", X)
    print("Y: ", Y)'''
    
    ''' X_training, Y_training = split_training_data(X, Y, split)
    X_testing, Y_testing = split_test_data(X, Y, split, end)

    X_training = np.array(X_training)
    Y_training = np.array(Y_training)
    X_testing = np.array(X_testing)
    Y_testing = np.array(Y_testing)'''

    '''print("X_training: ", X_training)
    print("Y_training: ", Y_training)
    print("X_testing: ", X_testing)
    print("Y_testing: ", Y_testing)'''
    
    '''return X_training, Y_training, X_testing, Y_testing'''
    return X, Y, ate

def convert_to_binary(value):
    list_value=np.array(value)
    '''print(list_value)'''
    v0value = []
    for j in range(len(list_value)):
        if list_value[j] == True:
            v0value.append(1.0)
        if list_value[j] == False:
            v0value.append(0.0)
    return v0value
'''
def split_training_data(X, Y, split):
    X_training = [] 
    Y_training = []
    for i in range(len(X)):
        X_training.append(X[i][0:split])
    for j in range(len(Y)):
        Y_training.append(Y[j][0:split])
    return X_training, Y_training

def split_test_data(X, Y, split, end):
    X_testing = []
    Y_testing = []
    for i in range(len(X)):
        X_testing.append(X[i][split:end])
    for j in range(len(Y)):
        Y_testing.append(Y[j][split:end])
    return X_testing, Y_testing'''

def duplicar_dataset():
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
    # Value of the coefficient [BETA] (real effect)
    BETA = 10
    # Number of Common Causes
    NUM_COMMON_CAUSES = 500
    # Number of Instruments
    NUM_INSTRUMENTS = 499
    # Number of Samples
    NUM_SAMPLES = 1000
    # Treatment is Binary
    TREATMENT_IS_BINARY = True
    data = dowhy.datasets.linear_dataset(
        beta=BETA,
        num_common_causes=NUM_COMMON_CAUSES,
        num_instruments=NUM_INSTRUMENTS,
        num_samples=NUM_SAMPLES,
        treatment_is_binary=TREATMENT_IS_BINARY)
        
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
    ate = data['ate']
    '''print("ATE: ", ate)  '''
    dataset_dict = {}
    X0= []
    X1= []
    Y0= []
    Y1= []
    columns = dataset.columns.values
    for i in range(len(columns)):
        name = columns[i]
        value = dataset[name]
        dataset_dict[name] = list(value)
        if name != "y":
            '''print("X: ")
            print(name)'''
            if name == "v0":
                print(name)
                len_value = len(value)
                X0.append(sin_tratamiento(len_value))
                X1.append(con_tratamiento(len_value))
                ''' print("X0: ",X0)
                print("X1: ",X1)'''
            else:
                X1.append(dataset_dict[name])
                X0.append(dataset_dict[name])
                '''print("X0: ",X0)
                print("X1: ",X1)'''

            '''print(dataset_dict[name])'''
            
        if name == "y":
            '''print("Y: ")
            print(name)'''
            Y0.append(dataset_dict[name])
            Y1.append(dataset_dict[name])
            '''print(dataset_dict[name])'''
    '''split = int(NUM_SAMPLES/2)
    end = int(len(dataset_dict))'''

    X0 = np.array(X0)
    Y0 = np.array(Y0)
    X1 = np.array(X1)
    Y2 = np.array(Y1)

    '''print("X: ", X)
    print("Y: ", Y)'''
    
    ''' X_training, Y_training = split_training_data(X, Y, split)
    X_testing, Y_testing = split_test_data(X, Y, split, end)

    X_training = np.array(X_training)
    Y_training = np.array(Y_training)
    X_testing = np.array(X_testing)
    Y_testing = np.array(Y_testing)'''

    '''print("X_training: ", X_training)
    print("Y_training: ", Y_training)
    print("X_testing: ", X_testing)
    print("Y_testing: ", Y_testing)'''
    
    '''return X_training, Y_training, X_testing, Y_testing'''
    return X0, Y0, X1, Y1, ate

def sin_tratamiento(len_value):
    v0 = []
    for i in range(len_value):
        v0.append(0)
    return v0

def con_tratamiento(len_value):
    v0 = []
    for i in range(len_value):
        v0.append(1)
    return v0


                                
