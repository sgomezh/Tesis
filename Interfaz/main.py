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

def showCausalGraph():
    pass

def estimate():
    pass

def refute():
    pass

def getBartDataset():
    file = open ('bart_dataset.txt','r')
    path = file.read()
    file.close()
    return path

def getBartSettings():
    settings = {} 
    file = open ('bart_settings.txt','r')
    for line in file:
        c = '\n'
        new_line = line.replace(c,"")
        settings.append(new_line)
    print(settings)
    return settings


# ----------------------- SETTINGS ----------------------
main_page = MainWin()

# --- Main loop --- 
main_page.mainloop() 


