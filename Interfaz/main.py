#import statement
from ast import main
from classes.viewClass import MainWin
from tkinter import *
from matplotlib.pyplot import text
from rpy2.robjects import r
global dowhyDataset
global bartDataset
# ----------------------- FUNCTIONS ----------------------

def buildCausalModel():
    pass

def predict():
    pass

def RMSE():
    pass

def R2():
    pass

def variableImportance():
    pass

def ATE():
    pass

def showVariableImportance():
    pass

def showCausalGraph():
    pass

def createCausalGRaph():
    from dowhy import CausalModel
    import pandas as pd

    path = getDowhyDataset()
    data= pd.read_csv(path, header = None)
    settings = getDowhySettinngs()

    model=CausalModel(
        data = data,
        treatment=settings['treatment'],
        outcome=settings['outcome_column'],
        instruments=settings['instrument_variables'],
        common_causes=settings['common_causes']
        )
    model.view_model()
    from IPython.display import Image, display
    display(Image(filename="causal_model.png")) 

def showCausalGraph():
    pass

def estimate():
    pass

def refute():
    pass

def getDowhyDataset():
    file = open ('dowhy_dataset.txt','r')
    path = file.read()
    file.close()
    return path
    
def getBartDataset():
    file = open ('bart_dataset.txt','r')
    path = file.read()
    file.close()
    return path

def getDowhySettinngs(): 
    settings = {} 
    settings_list = []
    file = open ('dowhy_settings.txt','r')
    for line in file:
        c = '\n'
        new_line = line.replace(c,"")
        settings_list.append(new_line)
    for i in range(len(settings_list)):
        if i == 0:
            settings['estimation_option'] = settings_list[i]
        elif i == 1:
            settings['treatment_column'] = settings_list[i]
        elif i == 2:
            settings['outcome_column'] = settings_list[i]
        elif i == 3:
            settings['instrumental_variables'] = settings_list[i]
        elif i == 4:
            settings['common_causes'] = settings_list[i]
    print(settings)
    return settings


# ----------------------- SETTINGS ----------------------
main_page = MainWin()

# --- Main loop --- 
main_page.mainloop() 


