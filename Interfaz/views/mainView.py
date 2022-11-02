from tkinter import Tk, Canvas, Label, Button, scrolledtext, INSERT
from tkinter.font import Font
from PIL import Image, ImageTk
import classes.viewMethods as vm


class mainView(Tk):
    def __init__(self):
        super().__init__()
        self.update()
        # --- Titulo ---
        self.title("Causal Tool")
        # --- Icono ---
        self.icon = Image.open('Interfaz/img/icon.png')
        self.photo = ImageTk.PhotoImage(self.icon)
        self.iconphoto(False, self.photo)
        # --- Tamagno --- 
        self.geometry("1200x600")
        self.minsize(1200, 600)
        self.maxsize(1200, 600)
        # --- Color ---
        self.configure(background='#08013D')
        self.tittle_font = Font(family="Arabic Transparent", size=25, weight="bold")
        self.label_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.button_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.result_font = Font(family="Arabic Transparent", size=14)
        # ---------------------- INTERFACE ----------------------
        self.image = Image.open('Interfaz/img/causal_tool.png')
        # --- Crea el canvas principal --- 
        self.center_canvas = Canvas(self, width= 290, height= 60)
        self.center_canvas.pack()

        # --- Carga la imagen de logo en la ventana principal --- 
        self.img = (Image.open("Interfaz/img/causal_tool.png"))

        # --- Redimensiona la imagen --- 
        self.resized_image= self.img.resize((300,70), Image.ANTIALIAS)
        self.appLogo = ImageTk.PhotoImage(self.resized_image)
        self.center_canvas.create_image(0,0, anchor='nw', image=self.appLogo)

        # --- Label BART ---
        self.bart_label = Label(self, text="BART", font=self.tittle_font, bg='#08013D', fg='#FFFFFF')
        self.bart_label.place(x=75, y=80)

        # --- label DoWhy ---
        self.dowhy_label = Label(self, text="DoWhy", font=self.tittle_font, bg='#08013D', fg='#FFFFFF')
        self.dowhy_label.place(x=1010, y=80)

        # --- Botones BART ---
        self.build_bart_button = Button(self, text="Build Bart", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command = lambda: self.build_bart_button_clicked())
        self.build_bart_button.place(x=20, y= 150)

        self.predict_button = Button(self, text="Predict", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: self.predict_button_clicked())
        self.predict_button.place(x=20, y= 230)

        self.variable_importance_button = Button(self, text="Display variable \nimportance graph", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: self.variable_importance_button_clicked())
        self.variable_importance_button.place(x=20, y= 310)

        self.ate_button = Button(self, text="Get ATE", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3)
        self.ate_button.place(x=20, y= 390)

        # --- Scrolledtext para el centro ---
        self.text_area = scrolledtext.ScrolledText(self, width= 55, height= 20 ,bg='#FFFFFF', font = self.result_font)
        self.text_area.insert(INSERT, "Bienvenido a Causal Tool 1.0")
        self.text_area.place(x=300, y=100)

        # ---- Canvas para el centro ----
        self.result_canvas = Canvas(self, width = 620, height = 440, bg ='#FFFFFF')
        self.result_canvas.place(x= 300, y= 100)
        self.result_canvas.destroy()

        # --- Botones DoWhy ---
        self.causal_model_button = Button(self, text="Build causal model", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: self.causal_model_button_clicked())
        self.causal_model_button.place(x=970, y=150)

        self.causal_graph_button = Button(self, text="Display causal graph", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: self.causal_graph_button_clicked())
        self.causal_graph_button.place(x=970, y=230)

        self.estimate_effect_button = Button(self, text="Estimate effect", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command=lambda: self.estimate_effect_button_clicked())
        self.estimate_effect_button.place(x=970, y= 310)

        self.refute_button = Button(self, text="Refute estimation", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=3, command= lambda: self.refute_button_clicked())
        self.refute_button.place(x=970, y=390)

        self.reset_button = Button(self, text="Reset", bg="#B7B5C8", fg="black", font=self.button_font, width=20, height=1, command= lambda: vm.resetApp())
        self.reset_button.place(x=500, y=560)

        # --- Controlador de la vista --- 
        self.controller = None

    # Esta funcion actualiza el controlador
    def setController(self, controller):
        self.controller = controller
    
    def build_bart_button_clicked(self):
        self.controller.build_bart_button_clicked()

    def predict_button_clicked(self):
        self.controller.predict_button_clicked()

    def variable_importance_button_clicked(self):
        self.controller.variable_importance_button_clicked()

    def ate_button_clicked(self):
        self.controller.ate_button_clicked()

    def causal_model_button_clicked(self):
        self.controller.causal_model_button_clicked()

    def causal_graph_button_clicked(self):
        self.controller.causal_graph_button_clicked()

    def estimate_effect_button_clicked(self):
        self.controller.estimate_effect_button_clicked()

    def refute_button_clicked(self):
        self.controller.refute_button_clicked()

    def update_text(self, text):
        """
        Actualiza el texto del text area
        @param text: texto a mostrar
        Importante: El texto debe ser una lista, en donde cada elemento es una linea
        """
        if(self.result_canvas.winfo_exists()):
            self.result_canvas.destroy()

        if(self.text_area.winfo_exists() == 0):    
            self.text_area = scrolledtext.ScrolledText(self, width= 55, height= 20 ,bg='#FFFFFF', font = self.result_font)
            self.text_area.place(x=300, y=100)
        
        for line in text:
            self.text_area.insert(INSERT, "\n" + line)
        
        self.text_area.see("end")

        

    def update_image(self, image):
        """
        Actualiza la imagen del canvas
        @param image: imagen a mostrar
        Consulta: Deberia recibir la ruta de la imagen o la imagen en si?
        """
        if(self.text_area.winfo_exists()):
            self.text_area.destroy()

        self.result_canvas = Canvas(self, width = 620, height = 440, bg ='#FFFFFF')
        self.result_canvas.create_image(0,0, anchor='nw', image=image)
        self.result_canvas.place(x= 300, y= 100)
        
        