import classes.viewClass as vc
from tkinter import *
from tkinter import filedialog

# Agrega los métodos de la clase a la interfaz gráfica
def buildBartModelView(master):
    newWindow = vc.PopupWin(master, 800, 600)
    
    build_bart_model_label = Label(newWindow, text="Build BART Model", font=newWindow.tittle_font, bg='#08013D', fg='#FFFFFF')
    build_bart_model_label.place(x=250, y=20)

    dataset_label= Label(newWindow, text="Dataset path (csv, txt):", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    dataset_label.place(x=10, y=70)

    path_label = Label(newWindow, text="", font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)

    search_button = Button(newWindow, text="Search", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: filePickerBart(newWindow))
    search_button.place(x=670, y=95)

    # Checkbox for cross validation
    cross_validation_checkbox = Checkbutton(newWindow, text="Cross Validation", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', selectcolor="black")
    cross_validation_checkbox.place(x=10, y=130)

    # MCMC configuration
    # TODO: Agregar una fuente con subrayado
    mcmc_label = Label(newWindow, text="MCMC Configuration", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', underline=1)
    mcmc_label.place(x=20, y=180)
    
    # Number of Trees
    number_of_trees_label = Label(newWindow, text="Number of Trees:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    number_of_trees_label.place(x=20, y=220)

    number_of_trees_entry = Entry(newWindow, width=10)
    number_of_trees_entry.place(x=170, y=220)

    # Number of Burn-in
    number_of_burn_in_label = Label(newWindow, text="Number of \nBurn-in iterations:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
    number_of_burn_in_label.place(x=20, y=250)

    number_of_burn_in_entry = Entry(newWindow, width=10)
    number_of_burn_in_entry.place(x=170, y=270)

    # Number of iterations after burn-in
    number_of_iterations_after_burn_in_label = Label(newWindow, text="Number of iterations \nafter burn-in:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
    number_of_iterations_after_burn_in_label.place(x=20, y=300)

    number_of_iterations_after_burn_in_entry = Entry(newWindow, width=10)
    number_of_iterations_after_burn_in_entry.place(x=170, y=320)

    # Prior configuration
    prior_label = Label(newWindow, text="Prior Configuration", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', underline=1)
    prior_label.place(x=20, y=360)

    # Alpha
    alpha_label = Label(newWindow, text="Alpha:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
    alpha_label.place(x=65, y=400)

    alpha_entry = Entry(newWindow, width=10)
    alpha_entry.place(x=170, y=400)

    # Beta
    beta_label = Label(newWindow, text="Beta:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    beta_label.place(x=65, y=430)

    beta_entry = Entry(newWindow, width=10)
    beta_entry.place(x=170, y=430)

    # K
    k_label = Label(newWindow, text="K:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    k_label.place(x=75, y=460)

    k_entry = Entry(newWindow, width=10)
    k_entry.place(x=170, y=460)

    # # Q
    # q_label = Label(newWindow, text="Q:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    # q_label.place(x=10, y=400)

    # q_entry = Entry(newWindow, width=10)
    # q_entry.place(x=150, y=400)

    # # nu
    # nu_label = Label(newWindow, text="nu:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    # nu_label.place(x=10, y=430)

    # nu_entry = Entry(newWindow, width=10)
    # nu_entry.place(x=150, y=430)

    # # Metropolis Hastings configuration
    # metropolis_hastings_label = Label(newWindow, text="Metropolis Hastings Configuration", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', underline=1)
    # metropolis_hastings_label.place(x=10, y=460)

    # # Grow percentage:
    # grow_percentage_label = Label(newWindow, text="Grow percentage:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    # grow_percentage_label.place(x=10, y=490)

    # grow_percentage_entry = Entry(newWindow, width=10)
    # grow_percentage_entry.place(x=150, y=490)

    # # Prune percentage:
    # prune_percentage_label = Label(newWindow, text="Prune percentage:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    # prune_percentage_label.place(x=10, y=520)

    # prune_percentage_entry = Entry(newWindow, width=10)
    # prune_percentage_entry.place(x=150, y=520)

    # # Change percentage:
    # change_percentage_label = Label(newWindow, text="Change percentage:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    # change_percentage_label.place(x=10, y=550)

    # change_percentage_entry = Entry(newWindow, width=10)
    # change_percentage_entry.place(x=150, y=550)

    # # Save button
    # save_button = Button(newWindow, text="Save", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: saveConfiguration(newWindow))
    # save_button.place(x=10, y=580)


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
def predictWindow(master):
    newWindow = vc.PopupWin(master, 800, 200)
    build_causal_model_label = Label(newWindow, text="Predict", font=newWindow.tittle_font, bg='#08013D', fg='#FFFFFF')
    build_causal_model_label.place(x=340, y=20)

    dataset_label= Label(newWindow, text="Dataset path (csv, txt):", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    dataset_label.place(x=10, y=70)

    path_label = Label(newWindow, text="", font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)

    search_button = Button(newWindow, text="Search", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: filePickerPredict(newWindow))
    search_button.place(x=670, y=95)

    search_button = Button(newWindow, text="Save", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1)
    search_button.place(x=350, y=150)

def filePickerDowhy(newWindow):
    file_path = filedialog.askopenfilename()
    path_label = Label(newWindow, text=file_path, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)
    f = open ('dowhy_dataset.txt','w')
    f.write(file_path)
    f.close()

def filePickerPredict(newWindow):
    file_path = filedialog.askopenfilename()
    path_label = Label(newWindow, text=file_path, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)
    f = open ('bart_ predict_dataset.txt','w')
    f.write(file_path)
    f.close()

def filePickerBart(newWindow):
    file_path = filedialog.askopenfilename()
    path_label = Label(newWindow, text=file_path, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
    path_label.place(x=5, y=100)
    f = open ('bart_dataset.txt','w')
    f.write(file_path)
    f.close()