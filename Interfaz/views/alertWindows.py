import tkinter.messagebox

def dowhyModelError():
    tkinter.messagebox.showerror(title="Error", message="Please set the DoWhy model before continue.")

def bartModelError():
    tkinter.messagebox.showerror(title="Error", message="Please set the BART model before continue.")

def estimateError():
    tkinter.messagebox.showerror(title="Error", message="Cannot estimate causal effect with DoWhy without setting up the model.")    

def refuteError():
    tkinter.messagebox.showerror(title="Error", message="This DoWhy model cannot be refuted without first estimating the causal effect.")
    
def datasetError():
    tkinter.messagebox.showerror(title="Error", message="No dataset selected.")
    
def dowhyDatasetError():
    tkinter.messagebox.showerror(title="Error", message="Invalid dataset for DoWhy.")

def treatmentError():
    tkinter.messagebox.showerror(title="Error", message="Bart model does not have a treatment variable.")