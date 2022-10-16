from select import select
import classes.viewClass as vc
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font

# Agrega los métodos de la clase a la interfaz gráfica
def buildBartModelView(newWindow, center_canvas):
    mcmc_coordinates = {"x": 60, "y": 180}
    prior_coordinates = {"x": 60, "y": 360}
    mh_coordinates = {"x": 450, "y": 180}

    config_font = Font(family="Arabic Transparent", size=15, weight="bold", underline=1)
    
    build_bart_model_label = Label(newWindow, text="Build BART Model", font=newWindow.tittle_font, bg='#08013D', fg='#FFFFFF')
    build_bart_model_label.place(x=250, y=20)

    dataset_label= Label(newWindow, text="Dataset path (csv, txt):", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    dataset_label.place(x=10, y=70)

    path_label = Label(newWindow, text="", font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=60, height=1)
    path_label.place(x=10, y=100)

    search_button = Button(newWindow, text="Search", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: filePickerBart(newWindow))
    search_button.place(x=670, y=95)

    # MCMC configuration
    # TODO: Agregar una fuente con subrayado
    mcmc_label = Label(newWindow, text="MCMC Configuration", font=config_font, bg='#08013D', fg='#FFFFFF', underline=1)
    mcmc_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"])
    
    # Number of Trees
    number_of_trees_label = Label(newWindow, text="Number of Trees:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    number_of_trees_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+40)

    number_of_trees_entry = Entry(newWindow, width=10)
    number_of_trees_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+40)

    # Number of Burn-in
    number_of_burn_in_label = Label(newWindow, text="Number of \nBurn-in iterations:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
    number_of_burn_in_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+70)

    number_of_burn_in_entry = Entry(newWindow, width=10)
    number_of_burn_in_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+90)

    # Number of iterations after burn-in
    number_of_iterations_after_burn_in_label = Label(newWindow, text="Number of iterations \nafter burn-in:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
    number_of_iterations_after_burn_in_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+120)

    number_of_iterations_after_burn_in_entry = Entry(newWindow, width=10)
    number_of_iterations_after_burn_in_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+140)

    # --- Prior configuration ---
    prior_label = Label(newWindow, text="Prior Configuration", font=config_font, bg='#08013D', fg='#FFFFFF', underline=1)
    prior_label.place(x=prior_coordinates["x"], y=prior_coordinates["y"])

    # Alpha
    alpha_label = Label(newWindow, text="Alpha:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
    alpha_label.place(x=prior_coordinates["x"]+40, y=prior_coordinates["y"]+40)

    alpha_entry = Entry(newWindow, width=10)
    alpha_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+40)

    # Beta
    beta_label = Label(newWindow, text="Beta:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    beta_label.place(x=prior_coordinates["x"]+47, y=prior_coordinates["y"]+70)

    beta_entry = Entry(newWindow, width=10)
    beta_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+70)

    # K
    k_label = Label(newWindow, text="K:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    k_label.place(x=prior_coordinates["x"]+58, y=prior_coordinates["y"]+100)

    k_entry = Entry(newWindow, width=10)
    k_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+100)

    # Q
    q_label = Label(newWindow, text="Q:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    q_label.place(x=prior_coordinates["x"]+58, y=prior_coordinates["y"]+130)

    q_entry = Entry(newWindow, width=10)
    q_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+130)

    # nu
    nu_label = Label(newWindow, text="nu:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    nu_label.place(x=prior_coordinates["x"]+55, y=prior_coordinates["y"]+160)

    nu_entry = Entry(newWindow, width=10)
    nu_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+160)

    # Metropolis Hastings configuration
    metropolis_hastings_label = Label(newWindow, text="Metropolis Hastings Configuration", font=config_font, bg='#08013D', fg='#FFFFFF', underline=1)
    metropolis_hastings_label.place(x=mh_coordinates["x"], y=mh_coordinates["y"])

    # Grow percentage:
    grow_percentage_label = Label(newWindow, text="Grow percentage:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    grow_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+40)

    grow_percentage_entry = Entry(newWindow, width=10)
    grow_percentage_entry.place(x=mh_coordinates["x"]+175, y=mh_coordinates["y"]+40)

    # Prune percentage:
    prune_percentage_label = Label(newWindow, text="Prune percentage:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    prune_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+70)

    prune_percentage_entry = Entry(newWindow, width=10)
    prune_percentage_entry.place(x=mh_coordinates["x"]+175, y=mh_coordinates["y"]+70)

    # Change percentage:
    change_percentage_label = Label(newWindow, text="Change percentage:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    change_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+100)

    change_percentage_entry = Entry(newWindow, width=10)
    change_percentage_entry.place(x=mh_coordinates["x"]+175, y=mh_coordinates["y"]+100)

    # Checkbox for cross validation
    cross_validation = IntVar()

    def activate_cross_validation():
        print(cross_validation.get())
        if (cross_validation.get() == 1):
            # Block all entrys except for k and nu
            number_of_burn_in_entry.config(state=DISABLED, disabledbackground='grey')
            number_of_iterations_after_burn_in_entry.config(state=DISABLED, disabledbackground='grey')
            change_percentage_entry.config(state=DISABLED, disabledbackground='grey')
            grow_percentage_entry.config(state=DISABLED, disabledbackground='grey')
            prune_percentage_entry.config(state=DISABLED, disabledbackground='grey')
            alpha_entry.config(state=DISABLED, disabledbackground='grey')
            beta_entry.config(state=DISABLED, disabledbackground='grey')
            q_entry.config(state=DISABLED, disabledbackground='grey')
            k_entry.config(state=NORMAL, disabledbackground='grey')
            nu_entry.config(state=NORMAL, disabledbackground='grey')
        else:
            # Else unblock all entrys
            number_of_burn_in_entry.config(state=NORMAL)
            number_of_iterations_after_burn_in_entry.config(state=NORMAL)
            change_percentage_entry.config(state=NORMAL)
            grow_percentage_entry.config(state=NORMAL)
            prune_percentage_entry.config(state=NORMAL)
            alpha_entry.config(state=NORMAL)
            beta_entry.config(state=NORMAL)
            q_entry.config(state=NORMAL)
            k_entry.config(state=NORMAL)
            nu_entry.config(state=NORMAL)

    cross_validation_checkbox = Checkbutton(newWindow, text="Cross Validation", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', selectcolor="black", variable = cross_validation, command=activate_cross_validation)
    cross_validation_checkbox.place(x=10, y=130)

    # Save button
    save_button = Button(newWindow, text="Save", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command=lambda: [
        saveBartConfig(cross_validation.get(),
                        number_of_trees_entry.get(), 
                        number_of_burn_in_entry.get(),
                        number_of_iterations_after_burn_in_entry.get(),
                        alpha_entry.get(),
                        beta_entry.get(),
                        k_entry.get(),
                        q_entry.get(),
                        nu_entry.get(),
                        grow_percentage_entry.get(),
                        prune_percentage_entry.get(),
                        change_percentage_entry.get()
                        ), newWindow.destroy()])
    save_button.place(x=330, y=550)


def saveBartConfig(crossValidation, numberOfTrees, numberOfBurnIn, numberOfIterationsAfterBurnIn, alpha, beta, k, q, nu, growPercentage, prunePercentage, changePercentage):
    f = open ('dowhy_settings.txt','w')
    if (crossValidation == 1):
        f.write(str(crossValidation))
        f.write("\n")
        f.write(str(numberOfTrees))
        f.write("\n")
        f.write(str(k))
        f.write("\n")
        f.write(str(nu))
        f.write("\n")
    if (crossValidation == 0):
        f.write(str(crossValidation))
        f.write("\n")
        f.write(str(numberOfTrees))
        f.write("\n")
        f.write(str(numberOfBurnIn))
        f.write("\n")
        f.write(str(numberOfIterationsAfterBurnIn))
        f.write("\n")
        f.write(str(alpha))
        f.write("\n")
        f.write(str(beta))
        f.write("\n")
        f.write(str(k))
        f.write("\n")
        f.write(str(q))
        f.write("\n")
        f.write(str(nu))
        f.write("\n")
        f.write(str(growPercentage))
        f.write("\n")
        f.write(str(prunePercentage))
        f.write("\n")
        f.write(str(changePercentage))
        f.write("\n")
    f.close()

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

    dataset_label= Label(newWindow, text="Effect estimation method:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    dataset_label.place(x=10, y=150)

    estimation_option = IntVar()

    linear_regression_option = Radiobutton(newWindow, text="Linear Regression", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF',padx = 20, variable=estimation_option, value=0, selectcolor="black")
    linear_regression_option.place(x=0, y=180)

    score_matching_option = Radiobutton(newWindow, text="Score Matching", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', variable=estimation_option, value=1, selectcolor="black")
    score_matching_option.place(x=200, y=180)

    score_weighting_option = Radiobutton(newWindow, text="Score Weighting", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', variable=estimation_option, value=2, selectcolor="black")
    score_weighting_option.place(x=400, y=180)

    DML_option = Radiobutton(newWindow, text="DML", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF', variable=estimation_option, value=3, selectcolor="black")
    DML_option.place(x=600, y=180)


    treatment_column_label= Label(newWindow, text="Treatment column:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    treatment_column_label.place(x=10, y=250)

    treatment_column_entry = Entry(newWindow, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=20, justify='left')
    treatment_column_entry.place(x=200, y=250)

    outcome_column_label= Label(newWindow, text="Outcome column:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    outcome_column_label.place(x=10, y=300)

    outcome_column_entry = Entry(newWindow, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=20, justify='left')
    outcome_column_entry.place(x=200, y=300)

    intrumental_variables_label= Label(newWindow, text="Instrumental Variables:", font=newWindow.label_font, bg='#08013D', fg='#FFFFFF')
    intrumental_variables_label.place(x=10, y=350)

    intrumental_variables_entry = Entry(newWindow, font=newWindow.label_font, bg='#FFFFFF', fg='#000000', width=20, justify='left')
    intrumental_variables_entry.place(x=200, y=350)

    save_button = Button(newWindow, text="Save", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: [saveSettingsDowhy(treatment_column_entry.get(), outcome_column_entry.get(), intrumental_variables_entry.get(), estimation_option.get()), newWindow.destroy()])
    save_button.place(x=350, y=450)


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

    predict_button = Button(newWindow, text="Predict", font=newWindow.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1)
    predict_button.place(x=350, y=150)

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

def saveSettingsDowhy(treatment_column, outcome_column, instrumental_variables, estimation_option):
    f = open ('dowhy_settings.txt','w')
    f.write(str(estimation_option))
    f.write("\n")
    f.write(treatment_column)
    f.write("\n")
    f.write(outcome_column)
    f.write("\n")
    f.write(instrumental_variables)
    f.close()