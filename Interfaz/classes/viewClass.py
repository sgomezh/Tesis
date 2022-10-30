from tkinter import Toplevel, Tk, Canvas, Label, Button, StringVar, Entry, filedialog, OptionMenu
from tkinter.font import Font
from PIL import Image, ImageTk
import classes.viewMethods as vm
from views.bartView import BartView
from views.doWhyView import DoWhyView

class BartApp():
    def __init__(self, parent):
        super().__init__()
        # Coordenadas de los widgets
        self.model = parent.model
        self.view = BartView(parent.mainView, self.model.bartSettings, 800, 600)
        self.controller = parent.controller

        self.view.set_controller(self.controller)

class DoWhyApp:
    def __init__(self, parent):
        self.model = parent.model
        self.view = DoWhyView(parent.mainView, 800, 600)
        self.controller = parent.controller
        
        self.view.set_controller(self.controller)

