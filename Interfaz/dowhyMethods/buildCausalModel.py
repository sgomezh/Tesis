from tkinter import filedialog
from tkinter import *

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