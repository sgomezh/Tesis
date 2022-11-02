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
    showRefuteResults(refute_results)

def showRefuteResults(refute_results):
    from tkinter import scrolledtext, INSERT
    from tkinter.font import Font

    result_font = Font(family="Arabic Transparent", size=14)
    
    text_area = scrolledtext.ScrolledText( width= 55, height= 20 ,bg='#FFFFFF', font = result_font)
    text_area.insert(INSERT, refute_results)
    text_area.place(x=300, y=100)