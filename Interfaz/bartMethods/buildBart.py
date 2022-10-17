from asyncio import subprocess
from tkinter import filedialog, Label, Entry, Button, Text
from tkinter.font import Font
from tkinter import filedialog
from rpy2.robjects import r
from rpy2.robjects.packages import importr
import pandas as pd

# Configuracion de la ventana para construir el BART
def buildBartModel(dataset, settings):
    config = getBartSettings()
    
    if config['cross_validation'] == '1':
        subprocess.call("bartMethods/buildBartScript.r -f " 
                            + dataset + " -n " + config['number_of_trees'] +
                            " -k " + config['k'] + " -nu " + config['nu'] + 
                            " -r " + config['responseVar'] + "-q " + config['q'] + " - burn " 
                            + config['burn_in'] + " -pburn " + config['iter_after_burn_in'] +, 
                            shell=True)



def getBartSettings():
    setting_list = []
    settings = {}
    file = open ('D:\Escritorio\Codigo\Tesis\\bart_settings.txt','r')
    for line in file:
        c = '\n'
        new_line = line.replace(c,"")
        setting_list.append(new_line)
    
    
    if setting_list[0] == '1': #Con CV
        for i in range(len(setting_list)):
            if i == 0:
                settings['cross_validation'] = setting_list[0]
            elif i == 1:
                settings['number_of_trees'] = setting_list[1]
            elif i == 2:
                settings['k'] = setting_list[2]
            elif i == 3:
                settings['nu'] = setting_list[3]
            elif i == 4:
                settings['responseVar'] = setting_list[4]
    elif setting_list[0] == '0': #Sin CV
        for i in range(len(setting_list)):
            if i == 0:
                settings['cross_validation'] = setting_list[0]
            elif i == 1:
                settings['number_of_trees'] = setting_list[1]
            elif i == 2:
                settings['burn_in_iter'] = setting_list[2]
            elif i == 3:
                settings['iter_after_burn_in'] = setting_list[3]
            elif i == 4:
                settings['alpha'] = setting_list[4]
            elif i == 5:
                settings['beta'] = setting_list[5]
            elif i == 6:
                settings['k'] = setting_list[6]
            elif i == 7:
                settings['q'] = setting_list[7]
            elif i == 8:
                settings['nu'] = setting_list[8]
            elif i == 9:
                settings['grow'] = setting_list[9]
            elif i == 10:
                settings['prune'] = setting_list[10]
            elif i == 11:
                settings['change'] = setting_list[11]
            elif i == 12:
                settings['responseVar'] = setting_list[12]

    return settings
    
    

buildBartModel("D:\Escritorio\Codigo\Tesis\\automobile.csv", "D:\Escritorio\Codigo\Tesis\\bart_settings.txt")