import tkinter as tk
from tkinter import BooleanVar, DoubleVar, IntVar, Label, Button, Entry, Toplevel, filedialog, StringVar, OptionMenu, Scale, HORIZONTAL
from tkinter.font import Font
from PIL import Image, ImageTk

class BartView(Toplevel):
    def __init__(self, parent, defaultSettings, width, height):
        super(BartView, self).__init__(parent)
        self.controller = None
        # --- Configuracion de la ventana ---
        self.transient(parent)
        self.title("Causal Tool")
        self.geometry(str(width) + "x" + str(height))
        icon = Image.open('Interfaz/icon.png')
        photo = ImageTk.PhotoImage(icon)
        self.wm_iconphoto(False, photo)
        self.minsize(width, height)
        self.maxsize(width, height)
        self.configure(bg='#08013D')

        # --- Fuentes ---
        self.title_font = Font(family="Arabic Transparent", size=25, weight="bold")
        self.label_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.response_font = Font(family="Arabic Transparent", size=10, weight="bold")
        self.button_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.result_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.config_font = Font(family="Arabic Transparent", size=12, weight="bold")

        # --- Coordenadas de los widgets ---
        mcmc_coordinates = {"x": 60, "y": 180}
        prior_coordinates = {"x": 60, "y": 360}
        mh_coordinates = {"x": 450, "y": 180}
        cv_coordinates = {"x": 20, "y": 132}

        self.settings = {}
        self.col_names = []

        # --- Titulo principal ---
        build_bart_model_label = Label(self, text="Build BART Model", font=self.title_font, bg='#08013D', fg='#FFFFFF')
        build_bart_model_label.place(x=250, y=20)

        # --- Widget: dataset picker ---
        self.dataset_label= Label(self, text="Dataset path (csv, txt):", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.dataset_label.place(x=10, y=70)

        self.path_label = Label(self, text="", font=self.label_font, bg='#FFFFFF', fg='#000000', width=60, height=1)
        self.path_label.place(x=10, y=100)

        self.search_button = Button(self, text="Search", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: self.search_button_clicked())
        self.search_button.place(x=670, y=95)

        # --- Widget: target picker ---
        self.response_label = Label(self, text="Response variable:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.response_label.place(x=200, y=132)
        
        self.settings['response'] = StringVar(value=defaultSettings['response'])
        self.response_option = OptionMenu(self, self.settings['response'], self.col_names)
        self.response_option.place(x=360, y=130)
        self.response_option.config(font=self.response_font, bg='#FFFFFF', fg='#000000', width=13, height=1)

        # --- Widget: Cross-validation checkbox ---
        self.settings['cv'] = BooleanVar()
        self.cv_label = Label(self, text="Cross-validation:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.cv_label.place(x=cv_coordinates['x'], y=cv_coordinates['y'])
        self.cv_checkbox = tk.Checkbutton(self, bg='#08013D', variable=self.settings['cv'], command=lambda: self.checkbox_clicked())
        self.cv_checkbox.place(x=cv_coordinates['x']+135, y=cv_coordinates['y'])

        # --- Titulo: Configuracion MCMC ---
        self.mcmc_label = Label(self, text="MCMC Configuration", font=self.config_font, bg='#08013D', fg='#FFFFFF', underline=1)
        self.mcmc_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"])
        
        # --- Widget: Numero de arboles ---
        self.number_of_trees_label = Label(self, text="Number of Trees:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.number_of_trees_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+40)

        self.settings['n_trees'] = IntVar(value=defaultSettings['n_trees'])
        self.number_of_trees_entry = Entry(self, textvariable=self.settings['n_trees'], width=10, disabledbackground='grey')
        self.number_of_trees_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+40)

        # --- Widget: Numero de iteraciones para el burn-in ---
        self.number_of_burn_in_label = Label(self, text="Number of \nBurn-in iterations:", font=self.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
        self.number_of_burn_in_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+70)

        self.settings['burn_in_iter'] = IntVar(value=defaultSettings['burn_in_iter'])
        self.number_of_burn_in_entry = Entry(self, textvariable=self.settings['burn_in_iter'], width=10, disabledbackground='grey')
        self.number_of_burn_in_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+90)

        # --- Widget: Numero de iteraciones post burn-in ---
        self.number_of_iterations_after_burn_in_label = Label(self, text="Number of iterations \nafter burn-in:", font=self.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
        self.number_of_iterations_after_burn_in_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+120)

        self.settings['after_burn_in_iter'] = IntVar(value=defaultSettings['after_burn_in_iter'])
        self.number_of_iterations_after_burn_in_entry = Entry(self, textvariable=self.settings['after_burn_in_iter'], width=10, disabledbackground='grey')
        self.number_of_iterations_after_burn_in_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+140)

        # --- Titulo: Configuracion de probabilidades priori ---
        self.prior_label = Label(self, text="Prior Configuration", font=self.config_font, bg='#08013D', fg='#FFFFFF', underline=1)
        self.prior_label.place(x=prior_coordinates["x"], y=prior_coordinates["y"])

        # --- Widget: Hiperparametro alpha ---
        self.alpha_label = Label(self, text="Alpha:", font=self.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
        self.alpha_label.place(x=prior_coordinates["x"]+40, y=prior_coordinates["y"]+40)

        self.settings['alpha'] = DoubleVar(value=defaultSettings['alpha'])
        self.alpha_entry = Entry(self,textvariable=self.settings['alpha'], width=10, disabledbackground='grey')
        self.alpha_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+40)

        # --- Widget: Hiperparametro beta ---
        self.beta_label = Label(self, text="Beta:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.beta_label.place(x=prior_coordinates["x"]+47, y=prior_coordinates["y"]+70)

        self.settings['beta'] = IntVar(value=defaultSettings['beta'])
        self.beta_entry = Entry(self, textvariable=self.settings['beta'], width=10, disabledbackground='grey')
        self.beta_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+70)

        # --- Widget: Hiperparametro K ---
        self.k_label = Label(self, text="K:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.k_label.place(x=prior_coordinates["x"]+58, y=prior_coordinates["y"]+100)

        self.settings['k'] = IntVar(value=defaultSettings['k'])
        self.k_entry = Entry(self, textvariable=self.settings['k'], width=10, disabledbackground='grey')
        self.k_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+100)

        # --- Widget: Hiperparametro q ---
        self.q_label = Label(self, text="Q:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.q_label.place(x=prior_coordinates["x"]+58, y=prior_coordinates["y"]+130)

        self.settings['q'] = DoubleVar(value=defaultSettings['q'])
        self.q_entry = Entry(self, textvariable=self.settings['q'], width=10, disabledbackground='grey')
        self.q_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+130)

        # --- Widget: Hiperparametro nu ---
        self.nu_label = Label(self, text="nu:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.nu_label.place(x=prior_coordinates["x"]+55, y=prior_coordinates["y"]+160)

        self.settings['nu'] = IntVar(value=defaultSettings['nu'])
        self.nu_entry = Entry(self, textvariable=self.settings['nu'], width=10, disabledbackground='grey')
        self.nu_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+160)

        # --- Titulo: Configuracion Metropolis Hastings ---
        self.metropolis_hastings_label = Label(self, text="Metropolis Hastings Configuration", font=self.config_font, bg='#08013D', fg='#FFFFFF', underline=1)
        self.metropolis_hastings_label.place(x=mh_coordinates["x"], y=mh_coordinates["y"])

        # --- Widget: Grow percentage ---
        self.grow_percentage_label = Label(self, text="Grow weight:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.grow_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+40)

        self.settings['grow'] = IntVar(value=defaultSettings['grow'])
        self.grow_scale = Scale(self, from_=0, to=100, length=200, bg='#08013D', fg='#FFFFFF', orient = HORIZONTAL, variable=self.settings['grow'])
        self.grow_scale.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+65)

        # --- Widget: Prune percentage ---
        self.prune_percentage_label = Label(self, text="Prune weight:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.prune_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+120)

        self.settings['prune'] = IntVar(value=defaultSettings['prune'])
        self.prune_scale = Scale(self, from_=0, to=100, length=200, bg='#08013D', fg='#FFFFFF', orient = HORIZONTAL, variable=self.settings['prune'])
        self.prune_scale.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+145)

        # --- Widget: Change percentage ---
        self.change_percentage_label = Label(self, text="Change weight:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.change_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+200)

        self.settings['change'] = IntVar(value=defaultSettings['change'])
        self.change_scale = Scale(self, from_=0, to=100, length=200, bg='#08013D', fg='#FFFFFF', orient = HORIZONTAL, variable=self.settings['change'])
        self.change_scale.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+225)

        # --- Widget: Build button ---
        self.build_button = Button(self, text="Build", font=self.button_font, bg='#FFFFFF', fg='#000000', command= lambda: self.build_button_clicked())
        self.build_button.place(x=300, y=550)

    def checkbox_clicked(self):
        if self.settings['cv'].get():
            self.number_of_trees_entry.config(state='disabled')
            self.number_of_burn_in_entry.config(state='disabled')
            self.number_of_iterations_after_burn_in_entry.config(state='disabled')
            self.alpha_entry.config(state='disabled')
            self.beta_entry.config(state='disabled')
            self.k_entry.config(state='disabled')
            self.q_entry.config(state='disabled')
            self.nu_entry.config(state='disabled')
            self.grow_scale.config(state='disabled')
            self.change_scale.config(state='disabled')
            self.prune_scale.config(state='disabled')
        else:
            self.number_of_trees_entry.config(state='normal')
            self.number_of_burn_in_entry.config(state='normal')
            self.number_of_iterations_after_burn_in_entry.config(state='normal')
            self.alpha_entry.config(state='normal')
            self.beta_entry.config(state='normal')
            self.k_entry.config(state='normal')
            self.q_entry.config(state='normal')
            self.nu_entry.config(state='normal')
            self.grow_scale.config(state='normal')
            self.grow_scale.config(state='normal')
            self.grow_scale.config(state='normal')

    # Actualiza el controlador
    def set_controller(self, controller):
        self.controller = controller

    # FilePicker
    def search_button_clicked(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.settings['file_path'] = file_path
            self.path_label.config(text=self.settings['file_path'])
            col_names = self.controller.get_col_names(self.settings['file_path'])
            # Update response variable optionmenu
            menu = self.response_option['menu']
            menu.delete(0, 'end')
            for name in col_names:
                menu.add_command(label=name, command=lambda value=name: self.settings['response'].set(value))
        else:
            raise Exception("No se selecciono ningun archivo")

    # Build button
    def build_button_clicked(self):
        if self.controller is not None:
            self.controller.store_settings(self.settings)
            self.controller.buildBart()


class PredictView(Toplevel):
    def __init__(self, parent):
        super(PredictView, self).__init__(parent)
        self.controller = parent.controller
        self.parent = parent

        # --- Fuentes ---
        self.title_font = Font(family="Arabic Transparent", size=25, weight="bold")
        self.label_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.response_font = Font(family="Arabic Transparent", size=10, weight="bold")
        self.button_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.result_font = Font(family="Arabic Transparent", size=12, weight="bold")
        self.config_font = Font(family="Arabic Transparent", size=12, weight="bold")
        
        # --- Configuracion de la ventana ---
        self.transient(parent)
        self.title("Causal Tool")
        self.geometry("800x200")
        icon = Image.open('Interfaz/icon.png')
        photo = ImageTk.PhotoImage(icon)
        self.wm_iconphoto(False, photo)
        self.minsize(800, 200)
        self.maxsize(800, 200)
        self.configure(bg='#08013D')

        self.build_causal_model_label = Label(self, text="Predict", font=self.title_font, bg='#08013D', fg='#FFFFFF')
        self.build_causal_model_label.place(x=340, y=20)

        self.dataset_label= Label(self, text="Dataset path (csv, txt):", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.dataset_label.place(x=10, y=70)

        self.path_label = Label(self, text="", font=self.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
        self.path_label.place(x=5, y=100)

        self.search_button = Button(self, text="Search", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: self.filePickerPredict())
        self.search_button.place(x=670, y=95)

        self.predict_button = Button(self, text="Predict", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: self.predict_button_clicked())
        self.predict_button.place(x=350, y=150)

    def predict_button_clicked(self):
        if self.controller is not None:
            self.controller.predictBart(self.file_path)


    def filePickerPredict(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.path_label.config(text=self.file_path)
        else:
            raise Exception("No se selecciono ningun archivo")

