from tkinter import Toplevel, Tk, Canvas, Label, Button, StringVar, Entry, filedialog, OptionMenu
from tkinter.font import Font
from PIL import Image, ImageTk
import classes.viewMethods as vm
import classes.bartModel as bm
import classes.bartView as bv
import classes.bartController as bc


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
        view = bv.BartView(parent, 800, 600)
        model = bm.bartModel()
        controller = bc.bartController(model, view)

        view.set_controller(controller)


# class PopupWin(Toplevel):
#     def __init__(self, master, width, height):
#         super(PopupWin, self).__init__(master)
#         self.transient(master)
#         self.title("Causal Tool")
#         self.geometry(str(width) + "x" + str(height))
#         icon = Image.open('Interfaz/icon.png')
#         photo = ImageTk.PhotoImage(icon)
#         self.wm_iconphoto(False, photo)
#         self.minsize(width, height)
#         self.maxsize(width, height)
#         self.configure(bg='#08013D')
#         self.tittle_font = Font(family="Arabic Transparent", size=25, weight="bold")
#         self.label_font = Font(family="Arabic Transparent", size=12, weight="bold")
#         self.button_font = Font(family="Arabic Transparent", size=12, weight="bold")
#         self.result_font = Font(family="Arabic Transparent", size=12, weight="bold")



    
# class alertWindow(PopupWin):
#     def __init__(self, master, title, message):
#         super(alertWindow, self).__init__(master, 300, 200)
#         self.title(title)
#         label = Label(self, text=message, font=vm.label_font, bg='#08013D', fg='#FFFFFF')
#         label.place(x=20, y=20)
#         button = Button(self, text="OK", bg="#B7B5C8", fg="black", font=vm.button_font, width=10, height=1, command= lambda: self.destroy())
#         button.place(x=100, y=100)
        
        