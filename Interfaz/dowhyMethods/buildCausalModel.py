from tkinter import filedialog
from tkinter import *
import dowhy
from dowhy import CausalModel
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
import sys
import warnings
from sklearn.exceptions import DataConversionWarning
from classes.MainApp.appModel import appModel


def generateCausalModel():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    #--------------------- Ignorar warnings ---------------------
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    warnings.filterwarnings(action='ignore', category=FutureWarning)

    path = getDowhyDataset()
    data= pd.read_csv(path, header = 0)
    settings = getDowhySettings()

    data = data.astype({"treatment":'bool'}, copy=False)


    # Create a causal model from the data and given common causes.
    model=CausalModel(
            data = data,
            treatment=settings['treatment_column'],
            outcome=settings['outcome_column'],
            common_causes=settings['common_causes'],
            instrumental= settings['instrumental_variables']
            )
    appModel.setDowhyModel(model)

def saveSettingsDowhy(treatment_column, outcome_column, instrumental_variables, common_causes, estimation_option):
    f = open ('dowhy_settings.txt','w')
    f.write(str(estimation_option))
    f.write("\n")
    f.write(treatment_column)
    f.write("\n")
    f.write(outcome_column)
    f.write("\n")
    f.write(instrumental_variables)
    f.write("\n")
    f.write(common_causes)
    f.close()
    
def filePickerDowhy(newWindow):
    file_path = filedialog.askopenfilename()
    path_label = Label(newWindow, text=file_path, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)
    f = open ('dowhy_dataset.txt','w')
    f.write(file_path)
    f.close()