from tkinter import Toplevel, Tk, Canvas, Label, Button, StringVar, Entry, filedialog, OptionMenu
from tkinter.font import Font
from PIL import Image, ImageTk
import classes.viewMethods as vm
import classes.BartApp.bartModel as bm
import classes.BartApp.bartView as bv
import classes.BartApp.bartController as bc


class MainWin(Tk):
    def __init__(self):
        super().__init__()
        self.update()
        # --- Titulo ---
        self.title("Causal Tool")
        # --- Icono ---
        icon = Image.open('Interfaz/icon.png')
        photo = ImageTk.PhotoImage(icon)
        self.iconphoto(False, photo)
        # --- Tamagno --- 
        self.geometry("1200x600")
        self.minsize(1200, 600)
        self.maxsize(1200, 600)
        # --- Color ---
        self.configure(background='#08013D')
        self.tittle_font = Font(family="Arabic Transparent", size=25, weight="bold")
        self.label_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.button_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.result_font = Font(family="Arabic Transparent", size=12, weight="bold")
        # ---------------------- INTERFACE ----------------------
        image = Image.open('Interfaz/causal_tool.png')
        #Create a canvas
        self.center_canvas = Canvas(self, width= 290, height= 60)
        self.center_canvas.pack()

        #Load an image in the script
        img = (Image.open("Interfaz/causal_tool.png"))

        #Resize the Image using resize method
        resized_image= img.resize((300,70), Image.ANTIALIAS)
        self.appLogo = ImageTk.PhotoImage(resized_image)

        #Add image to the Canvas Items
        self.center_canvas.create_image(0,0, anchor='nw', image=self.appLogo)

        # --- Label BART ---
        bart_label = Label(self, text="BART", font=self.tittle_font, bg='#08013D', fg='#FFFFFF')
        bart_label.place(x=75, y=80)

        # --- label DoWhy ---
        dowhy_label = Label(self, text="DoWhy", font=self.tittle_font, bg='#08013D', fg='#FFFFFF')
        dowhy_label.place(x=1010, y=80)

        # --- Botones BART ---
        button1 = Button(self, text="Build Bart", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command = lambda: BartApp(self))
        button1.place(x=20, y= 150)

        button2 = Button(self, text="Predict", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: vm.predictWindow(self))
        button2.place(x=20, y= 230)

        button3 = Button(self, text="Display variable \nimportance graph", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3)
        button3.place(x=20, y= 310)

        button4 = Button(self, text="Get ATE", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3)
        button4.place(x=20, y= 390)

        # --- Canvas resultados ---
        result_canvas = Canvas(self, width= 500, height= 400, bg='#FFFFFF')
        result_canvas.place(x=350, y=150)
        # --- Botones DoWhy ---
        button5 = Button(self, text="Build causal model", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: vm.buildCausalModel(self))
        button5.place(x=970, y=150)

        button6 = Button(self, text="Display causal graph", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: vm.createCausalGraph())
        button6.place(x=970, y=230)

        button7 = Button(self, text="Estimate effect", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3)
        button7.place(x=970, y= 310)

        button8 = Button(self, text="Refute estimation", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3)
        button8.place(x=970, y=390)

        button9 = Button(self, text="Reset", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=1, command= lambda: vm.resetApp())
        button9.place(x=500, y=560)

class BartApp():
    def __init__(self, parent):
        super().__init__()
        # Coordenadas de los widgets
        self.model = bm.bartModel()
        self.view = bv.BartView(parent, self.model.settings, 800, 600)
        self.controller = bc.bartController(self.model, self.view, parent)

        self.view.set_controller(self.controller)

    def predictWindow(self):
        self.view.predictWindow()


