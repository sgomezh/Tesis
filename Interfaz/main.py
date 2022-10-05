#import statement
from ast import main
import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk
# ----------------------- FUNCTIONS ----------------------
def predict():
    print_var = "Predict"
    result_label = tk.Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
def RMSE():
    print_var = "RMSE"
    result_label = tk.Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
def variableImportance():
    print_var = "Variable Importance"
    result_label = tk.Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
    showVariableImportance()
def ATE():
    print_var = "ATE"
    result_label = tk.Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
def showVariableImportance():
    pass
def causalGraph():
    import dowhy
    from dowhy import CausalModel
    import pandas as pd
    import numpy as np
    data= pd.read_csv("https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv", header = None)
    col =  ["treatment", "y_factual", "y_cfactual", "mu0", "mu1" ,]
    for i in range(1,26):
        col.append("x"+str(i))
    data.columns = col
    data = data.astype({"treatment":'bool'}, copy=False)
    # Create a causal model from the data and given common causes.
    model=CausalModel(
            data = data,
            treatment='treatment',
            outcome='y_factual',
            common_causes=["x"+str(i) for  i in range(1,26)]
            )
    model.view_model()
    from IPython.display import Image, display
    display(Image(filename="causal_model.png"))
    showCausalGraph()
    
def showCausalGraph():
    image = Image.open('causal_model.png')
    causal_graph = ImageTk.PhotoImage(image)
    label = tk.Label(main_page, image=causal_graph)
    label.image = causal_graph
    label.place(x=anchura/4, y=200)
def estimate():
    import dowhy
    from dowhy import CausalModel
    import pandas as pd
    import numpy as np
    data= pd.read_csv("https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv", header = None)
    col =  ["treatment", "y_factual", "y_cfactual", "mu0", "mu1" ,]
    for i in range(1,26):
        col.append("x"+str(i))
    data.columns = col
    data = data.astype({"treatment":'bool'}, copy=False)


    # Create a causal model from the data and given common causes.
    model=CausalModel(
            data = data,
            treatment='treatment',
            outcome='y_factual',
            common_causes=["x"+str(i) for  i in range(1,26)]
            )
    identified_estimand= model.identify_effect(proceed_when_unidentifiable=True)
    estimate_ = model.estimate_effect(identified_estimand,
                                method_name="backdoor.linear_regression") 
    print_var = str(estimate_)
    result_label = tk.Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
    return model, identified_estimand, estimate_
def refute():
    model, identified_estimand, estimate_ = estimate()
    refute_results=model.refute_estimate(identified_estimand, estimate_,
    method_name="random_common_cause")
    print_var = str(refute_results)
    result_label = tk.Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
# ----------------------- SETTINGS ----------------------

#create GUI Tk() variable
main_page = tk.Tk()
#set title
main_page.title("Causal Tool")
#set icon
icon = Image.open('Interfaz/icon.png')
photo = ImageTk.PhotoImage(icon)
main_page.wm_iconphoto(False, photo)
#set window size
main_page.state('zoomed')
#set window background color
main_page.configure(background='#08013D')
#obtain screen resolution
anchura = main_page.winfo_screenwidth()
altura  = main_page.winfo_screenheight()
# -------------------------------------
#set fonts
label_font = Font(family="Arabic Transparent", size=25, weight="bold")
button_font = Font(family="Arabic Transparent", size=12, weight="bold")
result_font = Font(family="Arabic Transparent", size=12, weight="bold")
# ---------------------- INTERFACE ----------------------
#image
image = Image.open('Interfaz/causal_tool.png')
logo = ImageTk.PhotoImage(image)
label = tk.Label(main_page, image=logo)
label.image = logo
label.place(x=anchura/3+50, y=10)
# -------------------------------------
#label BART
bart_label = tk.Label(main_page, text="BART", font=label_font, bg='#08013D', fg='#FFFFFF')
bart_label.place(x=60, y=180)
# -------------------------------------
#label DoWhy
dowhy_label = tk.Label(main_page, text="DoWhy", font=label_font, bg='#08013D', fg='#FFFFFF')
dowhy_label.place(x=anchura-180, y=180)
# -------------------------------------
#buttons BART
button2 = tk.Button(main_page, text="Predict", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command= predict)
button2.place(x=20, y= 250)

button3 = tk.Button(main_page, text="RMSE", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = RMSE)
button3.place(x=20, y= 330)

button4 = tk.Button(main_page, text="Variable \nImportance", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = variableImportance)
button4.place(x=20, y= 410)
'''
button5 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button5.place(x=20, y=370)

button6 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button6.place(x=20, y=450)

button7 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button7.place(x=20, y=530)

button8 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button8.place(x=20, y=610)'''
# -------------------------------------
# Result label
result_label = tk.Label(main_page, text="", font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
result_label.place(x=anchura/4, y=200)
# -------------------------------------
#buttons DoWhy
button2 = tk.Button(main_page, text="Get ATE", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = ATE)
button2.place(x=anchura-225, y=250)

button3 = tk.Button(main_page, text="GML Graph", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = causalGraph)
button3.place(x=anchura-225, y=330)

button4 = tk.Button(main_page, text="Estimate effect", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = estimate)
button4.place(x=anchura-225, y=410)

button5 = tk.Button(main_page, text="Refute result", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = refute)
button5.place(x=anchura-225, y= 490)
'''
button6 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button6.place(x=1150, y=450)

button7 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button7.place(x=1150, y=530)

button8 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button8.place(x=1150, y=610)'''
# -------------------------------------

#show window
main_page.mainloop() 


