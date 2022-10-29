
import classes.viewClass as vc
from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import Toplevel

class DoWhyView(Toplevel):
    def __init__(self, parent, width, height):
        super(DoWhyView, self).__init__(parent)
        # ---------Configuracion de la ventana ------------
        self.transient(parent)
        self.title("Causal Tool")
        self.geometry(str(width) + "x" + str(height))
        icon = Image.open('Interfaz/img/icon.png')
        photo = ImageTk.PhotoImage(icon)
        self.wm_iconphoto(False, photo)
        self.minsize(width, height)
        self.maxsize(width, height)
        self.configure(bg='#08013D')

        # ---------Configuracion de las fuentes ------------
        self.title_font = Font(family="Arabic Transparent", size=25, weight="bold")
        self.label_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.button_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.result_font = Font(family="Arabic Transparent", size=12, weight="bold")


        # ---------Configuracion de los elementos ------------
        self.build_causal_model_label = Label(self, text="Build Causal Model", font=self.title_font, bg='#08013D', fg='#FFFFFF')
        self.build_causal_model_label.place(x=250, y=20)

        self.dataset_label= Label(self, text="Dataset path (csv, txt):", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.dataset_label.place(x=10, y=70)

        self.path_label = Label(self, text="", font=self.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
        self.path_label.place(x=5, y=100)

        self.search_button = Button(self, text="Search", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: self.filePickerDowhy(self))
        self.search_button.place(x=670, y=95)

        self.dataset_label= Label(self, text="Effect estimation method:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.dataset_label.place(x=10, y=150)

        self.estimation_option = IntVar()

        self.linear_regression_option = Radiobutton(self, text="Linear Regression", font=self.label_font, bg='#08013D', fg='#FFFFFF',padx = 20, variable=self.estimation_option, value=0, selectcolor="black")
        self.linear_regression_option.place(x=0, y=180)

        self.score_matching_option = Radiobutton(self, text="Score Matching", font=self.label_font, bg='#08013D', fg='#FFFFFF', variable=self.estimation_option, value=1, selectcolor="black")
        self.score_matching_option.place(x=200, y=180)

        self.score_weighting_option = Radiobutton(self, text="Score Weighting", font=self.label_font, bg='#08013D', fg='#FFFFFF', variable=self.estimation_option, value=2, selectcolor="black")
        self.score_weighting_option.place(x=400, y=180)

        self.DML_option = Radiobutton(self, text="DML", font=self.label_font, bg='#08013D', fg='#FFFFFF', variable=self.estimation_option, value=3, selectcolor="black")
        self.DML_option.place(x=600, y=180)

        self.treatment_column_label= Label(self, text="Treatment column:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.treatment_column_label.place(x=10, y=250)

        self.treatment_column_entry = Entry(self, font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, justify='left')
        self.treatment_column_entry.place(x=200, y=250)

        self.outcome_column_label= Label(self, text="Outcome column:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.outcome_column_label.place(x=10, y=300)

        self.outcome_column_entry = Entry(self, font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, justify='left')
        self.outcome_column_entry.place(x=200, y=300)

        self.intrumental_variables_label= Label(self, text="Instrumental Variables:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.intrumental_variables_label.place(x=10, y=350)

        self.intrumental_variables_entry = Entry(self, font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, justify='left')
        self.intrumental_variables_entry.place(x=200, y=350)

        self.intrumental_variables_label= Label(self, text="Common Causes:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.intrumental_variables_label.place(x=10, y=400)

        self.common_causes_entry = Entry(self, font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, justify='left')
        self.common_causes_entry.place(x=200, y=400)

        self.save_button = Button(self, text="Save", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: [self.saveSettingsDowhy(self.treatment_column_entry.get(), self.outcome_column_entry.get(), self.intrumental_variables_entry.get(),  self.common_causes_entry.get(), self.estimation_option.get()), self.destroy()])
        self.save_button.place(x=350, y=450)

        self.controller = None

    def set_controller(self, controller):
        self.controller = controller