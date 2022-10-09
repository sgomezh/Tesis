#import statement
from ast import main
from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
from rpy2.robjects import r
# ----------------------- FUNCTIONS ----------------------
def build():
    newWindow = generateNewWindow(500, 500)
    
    # r('''
    # library(bartMachine)
    # print('12345')
    # ''')

def buildCausalModel():
    pass
def predict():
    r('''
    library(bartMachine)
    print('12345')
    ''')
def RMSE():
    print_var = "RMSE"
    result_label = Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
def variableImportance():
    print_var = "Variable Importance"
    result_label = Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
    showVariableImportance()
def ATE():
    print_var = "ATE"
    result_label = Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
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
    label = Label(main_page, image=causal_graph)
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
    result_label = Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)
    return model, identified_estimand, estimate_
def refute():
    model, identified_estimand, estimate_ = estimate()
    refute_results=model.refute_estimate(identified_estimand, estimate_,
    method_name="random_common_cause")
    print_var = str(refute_results)
    result_label = Label(main_page, text=print_var, font=result_font, bg='#FFFFFF', fg='#000000', width=100, height=20)
    result_label.place(x=anchura/4, y=200)

def generateNewWindow(width, height):
    newWindow = Toplevel(main_page)
    newWindow.title("Causal Tool")
    newWindow.geometry(str(width) + "x" + str(height))
    icon = Image.open('Interfaz/icon.png')
    photo = ImageTk.PhotoImage(icon)
    newWindow.wm_iconphoto(False, photo)
    newWindow.minsize(width, height)
    newWindow.maxsize(width, height)
    return newWindow
# ----------------------- SETTINGS ----------------------
#create GUI Tk() variable
main_page = Tk()
#set title
main_page.title("Causal Tool")
#set icon
icon = Image.open('Interfaz/icon.png')
photo = ImageTk.PhotoImage(icon)
main_page.wm_iconphoto(False, photo)
#set window size
main_page.geometry("1200x600")
main_page.minsize(1200, 600)
main_page.maxsize(1200, 600)
anchura = main_page.winfo_screenwidth()
altura  = main_page.winfo_screenheight()

#set window background color
main_page.configure(background='#08013D')
#obtain screen resolution

# -------------------------------------
#set fonts
label_font = Font(family="Arabic Transparent", size=25, weight="bold")
button_font = Font(family="Arabic Transparent", size=12, weight="bold")
result_font = Font(family="Arabic Transparent", size=12, weight="bold")
# ---------------------- INTERFACE ----------------------
#image
image = Image.open('Interfaz/causal_tool.png')
#Create a canvas
canvas= Canvas(main_page, width= 290, height= 60)
canvas.pack()

#Load an image in the script
img= (Image.open("Interfaz/causal_tool.png"))

#Resize the Image using resize method
resized_image= img.resize((300,70), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)

#Add image to the Canvas Items
canvas.create_image(0,0, anchor=NW, image=new_image)

# -------------------------------------
#label BART

bart_label = Label(main_page, text="BART", font=label_font, bg='#08013D', fg='#FFFFFF')
bart_label.place(x=75, y=80)
# -------------------------------------

#label DoWhy
dowhy_label = Label(main_page, text="DoWhy", font=label_font, bg='#08013D', fg='#FFFFFF')
dowhy_label.place(x=1010, y=80)

# -------------------------------------
#buttons BART
button1 = Button(main_page, text="Build Bart", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command= build)
button1.place(x=20, y= 150)

button2 = Button(main_page, text="Predict", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = predict)
button2.place(x=20, y= 230)

button3 = Button(main_page, text="Display variable \nimportance graph", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = variableImportance)
button3.place(x=20, y= 310)

button4 = Button(main_page, text="Get ATE", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = ATE)
button4.place(x=20, y= 390)

# -------------------------------------
# Result canvas
# TODO: Hay que poner la caja blanca en medio de la pantalla
result_canvas = Canvas(main_page, width= 500, height= 400, bg='#FFFFFF')
result_canvas.place(x=350, y=150)
# -------------------------------------
#buttons DoWhy
button5 = Button(main_page, text="Build causal model", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = buildCausalModel)
button5.place(x=970, y=150)

button6 = Button(main_page, text="Display causal graph", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = causalGraph)
button6.place(x=970, y=230)

button7 = Button(main_page, text="Estimate effect", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3, command = estimate)
button7.place(x=970, y= 310)

button8 = Button(main_page, text="Refute estimation", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button8.place(x=970, y=390)
'''
button9 = Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button9.place(x=1150, y=530)

button10 = Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button10.place(x=1150, y=610)'''
# -------------------------------------

#show window
main_page.mainloop() 


