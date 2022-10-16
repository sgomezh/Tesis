from tkinter import filedialog, Label, Entry, Button, Text
from tkinter.font import Font
from tkinter import filedialog
from rpy2.robjects import r
from rpy2.robjects.packages import importr
import rpy2

# Configuracion de la ventana para construir el BART
def buildBartModel(dataset, settings):
    bMachine = importr('bartMachine')
    data = rpy2.robjects.r['read.csv'](dataset)
    r.assign('data', data)
    r('print(data)')



def loadBartDataset(path):
    try:
        file = open ('bart_dataset.txt','w')
        file.write(path)
        file.close()
        print("Bart dataset path saved")
    except:
        print("Error saving Bart dataset path")
    
    

#buildBartModel("https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv", 1)