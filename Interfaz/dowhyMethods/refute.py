from tkinter import *
import sys
import warnings
from sklearn.exceptions import DataConversionWarning
from classes.MainApp.appModel import appModel

def refute(model, identified_estimand, estimate):
    #--------------------- Configuraciones de Encoder ---------------------
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    #--------------------- Ignorar warnings ---------------------
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    warnings.filterwarnings(action='ignore', category=FutureWarning)
    
    model = appModel.getDowhyModel()
    identified_estimand = appModel.getDowhyIdentifiedEstimand()
    estimate = appModel.getDowhyEstimate()

    refute_results=model.refute_estimate(identified_estimand, estimate,
            method_name="random_common_cause")

    appModel.setDowhyRefute(refute_results)
    print(refute_results)
