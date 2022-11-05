from tkinter import filedialog
from tkinter import *
from dowhy import CausalModel
import pandas as pd
import sys
import warnings
from sklearn.exceptions import DataConversionWarning

def generateCausalModel(doWhySettings):
    
#     # --------------------- Configuracion de encoder  ---------------------
#     sys.stdin.reconfigure(encoding='utf-8')
#     sys.stdout.reconfigure(encoding='utf-8')
#     warnings.filterwarnings(action='ignore', category=DataConversionWarning)
#     warnings.filterwarnings(action='ignore', category=FutureWarning)

    # --------------------- Leer archivo de datos ---------------------
    data = pd.read_csv(doWhySettings['file_path'], header = 0)
    #data = data.astype({"treatment":'bool'}, copy=False)

    # --------------------- Crea modelo causal ---------------------
    model=CausalModel(
            data = data,
            treatment=doWhySettings['treatment_column'],
            outcome=doWhySettings['outcome_column'],
            common_causes=doWhySettings['common_causes_column'],
            instruments= doWhySettings['instrumental_var_column'],
            )  

    return model

