from bartMethods.buildBart import buildBartView
import classes.viewClass as vc
from tkinter import *
from tkinter import filedialog

# Agrega los métodos de la clase a la interfaz gráfica
def buildBartModel(master):
    newWindow = vc.PopupWin(master, 500, 500)
    newWindow = buildBartView(newWindow)

def buildCausalModel(master):
    newWindow = vc.PopupWin(master, 800, 500)

    build_causal_model_label = Label(newWindow, text="Build Causal Model", font=newWindow.tittle_font, bg='#08013D', fg='#FFFFFF')
    build_causal_model_label.place(x=250, y=20)

    dataset_label= Label(newWindow, text="Dataset path (csv, txt):", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    dataset_label.place(x=10, y=70)

    path_label = Label(newWindow, text="", font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)

    search_button = Button(newWindow, text="Search", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: filePickerDowhy(newWindow))
    search_button.place(x=670, y=95)

    dataset_label= Label(newWindow, text="Efect estimation method:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    dataset_label.place(x=10, y=150)

    linear_regression_checkbox = Checkbutton(newWindow, text="Linear Regression", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    linear_regression_checkbox.place(x=10, y=180)

def filePickerDowhy(newWindow):
    file_path = filedialog.askopenfilename()
    path_label = Label(newWindow, text=file_path, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)
    f = open ('dowhy_dataset.txt','w')
    f.write(file_path)
    f.close()