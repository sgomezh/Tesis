from tkinter import *
import sys
import warnings
from sklearn.exceptions import DataConversionWarning

def refute(model, identified_estimand, estimate):
    #--------------------- Configuraciones de Encoder ---------------------
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    warnings.filterwarnings(action='ignore', category=FutureWarning)

    #--------------------- Refutar resultados con causas comunes ---------------------        
    refute_results=model.refute_estimate(identified_estimand, estimate,
            method_name="random_common_cause")
    text = str(refute_results).split("\n")
    return text

