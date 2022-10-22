# Este archivo contiene todas las vistas relacionadas a BART
import tkinter as tk
from tkinter import Label, Button, Entry, Toplevel, filedialog, StringVar, OptionMenu
from tkinter.font import Font
from PIL import Image, ImageTk

import classes.viewClass as vc

class BartView(Toplevel):
    def __init__(self, parent, width, height):
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
        
        self.settings['response'] = StringVar()
        self.response_option = OptionMenu(self, self.settings['response'], self.col_names)
        self.response_option.place(x=360, y=130)
        self.response_option.config(font=self.response_font, bg='#FFFFFF', fg='#000000', width=13, height=1)

        # --- Widget: Cross-validation checkbox ---
        self.settings['cv'] = tk.BooleanVar()
        print("Estado inicial: ", self.settings['cv'].get())
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

        self.settings['n_trees'] = StringVar()
        self.number_of_trees_entry = Entry(self, textvariable=self.settings['n_trees'], width=10, disabledbackground='grey')
        self.number_of_trees_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+40)

        # --- Widget: Numero de iteraciones para el burn-in ---
        self.number_of_burn_in_label = Label(self, text="Number of \nBurn-in iterations:", font=self.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
        self.number_of_burn_in_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+70)

        self.settings['burn_in_iter'] = StringVar()
        self.number_of_burn_in_entry = Entry(self, textvariable=self.settings['burn_in_iter'], width=10, disabledbackground='grey')
        self.number_of_burn_in_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+90)

        # --- Widget: Numero de iteraciones post burn-in ---
        self.number_of_iterations_after_burn_in_label = Label(self, text="Number of iterations \nafter burn-in:", font=self.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
        self.number_of_iterations_after_burn_in_label.place(x=mcmc_coordinates["x"], y=mcmc_coordinates["y"]+120)

        self.settings['after_burn_in_iter'] = StringVar()
        self.number_of_iterations_after_burn_in_entry = Entry(self, textvariable=self.settings['after_burn_in_iter'], width=10, disabledbackground='grey')
        self.number_of_iterations_after_burn_in_entry.place(x=mcmc_coordinates["x"]+150, y=mcmc_coordinates["y"]+140)

        # --- Titulo: Configuracion de probabilidades priori ---
        self.prior_label = Label(self, text="Prior Configuration", font=self.config_font, bg='#08013D', fg='#FFFFFF', underline=1)
        self.prior_label.place(x=prior_coordinates["x"], y=prior_coordinates["y"])

        # --- Widget: Hiperparametro alpha ---
        self.alpha_label = Label(self, text="Alpha:", font=self.label_font, bg='#08013D', fg='#FFFFFF', anchor="center")
        self.alpha_label.place(x=prior_coordinates["x"]+40, y=prior_coordinates["y"]+40)

        self.settings['alpha'] = StringVar()
        self.alpha_entry = Entry(self,textvariable=self.settings['alpha'], width=10, disabledbackground='grey')
        self.alpha_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+40)

        # --- Widget: Hiperparametro beta ---
        self.beta_label = Label(self, text="Beta:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.beta_label.place(x=prior_coordinates["x"]+47, y=prior_coordinates["y"]+70)

        self.settings['beta'] = StringVar()
        self.beta_entry = Entry(self, textvariable=self.settings['beta'], width=10, disabledbackground='grey')
        self.beta_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+70)

        # --- Widget: Hiperparametro K ---
        self.k_label = Label(self, text="K:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.k_label.place(x=prior_coordinates["x"]+58, y=prior_coordinates["y"]+100)

        self.settings['k'] = StringVar()
        self.k_entry = Entry(self, textvariable=self.settings['k'], width=10, disabledbackground='grey')
        self.k_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+100)

        # --- Widget: Hiperparametro q ---
        self.q_label = Label(self, text="Q:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.q_label.place(x=prior_coordinates["x"]+58, y=prior_coordinates["y"]+130)

        self.settings['q'] = StringVar()
        self.q_entry = Entry(self, textvariable=self.settings['q'], width=10, disabledbackground='grey')
        self.q_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+130)

        # --- Widget: Hiperparametro nu ---
        self.nu_label = Label(self, text="nu:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.nu_label.place(x=prior_coordinates["x"]+55, y=prior_coordinates["y"]+160)

        self.settings['nu'] = StringVar()
        self.nu_entry = Entry(self, textvariable=self.settings['nu'], width=10, disabledbackground='grey')
        self.nu_entry.place(x=prior_coordinates["x"]+150, y=prior_coordinates["y"]+160)

        # --- Titulo: Configuracion Metropolis Hastings ---
        self.metropolis_hastings_label = Label(self, text="Metropolis Hastings Configuration", font=self.config_font, bg='#08013D', fg='#FFFFFF', underline=1)
        self.metropolis_hastings_label.place(x=mh_coordinates["x"], y=mh_coordinates["y"])

        # --- Widget: Grow percentage ---
        self.grow_percentage_label = Label(self, text="Grow percentage:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.grow_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+40)

        self.settings['grow'] = StringVar()
        self.grow_percentage_entry = Entry(self, textvariable=self.settings['grow'], width=10, disabledbackground='grey')
        self.grow_percentage_entry.place(x=mh_coordinates["x"]+175, y=mh_coordinates["y"]+40)

        # --- Widget: Prune percentage ---
        self.prune_percentage_label = Label(self, text="Prune percentage:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.prune_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+70)

        self.settings['prune'] = StringVar()
        self.prune_percentage_entry = Entry(self, textvariable=self.settings['prune'], width=10, disabledbackground='grey')
        self.prune_percentage_entry.place(x=mh_coordinates["x"]+175, y=mh_coordinates["y"]+70)

        # --- Widget: Change percentage ---
        self.change_percentage_label = Label(self, text="Change percentage:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.change_percentage_label.place(x=mh_coordinates["x"]+10, y=mh_coordinates["y"]+100)

        self.settings['change'] = StringVar()
        self.change_percentage_entry = Entry(self, textvariable=self.settings['change   '], width=10, disabledbackground='grey')
        self.change_percentage_entry.place(x=mh_coordinates["x"]+175, y=mh_coordinates["y"]+100)

        # --- Widget: Build button ---
        self.build_button = Button(self, text="Build", font=self.button_font,  bg='#FFFFFF', fg='#000000', command=self.build_button_clicked())
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
            self.grow_percentage_entry.config(state='disabled')
            self.change_percentage_entry.config(state='disabled')
            self.prune_percentage_entry.config(state='disabled')
        else:
            self.number_of_trees_entry.config(state='normal')
            self.number_of_burn_in_entry.config(state='normal')
            self.number_of_iterations_after_burn_in_entry.config(state='normal')
            self.alpha_entry.config(state='normal')
            self.beta_entry.config(state='normal')
            self.k_entry.config(state='normal')
            self.q_entry.config(state='normal')
            self.nu_entry.config(state='normal')
            self.grow_percentage_entry.config(state='normal')
            self.change_percentage_entry.config(state='normal')
            self.prune_percentage_entry.config(state='normal')

    def set_controller(self, controller):
        self.controller = controller

    def store_settings(self):
        # Create a dictionary with the settings
        settings = {}
        for key in self.settings:
            settings[key] = self.settings[key].get()

        self.controller.store_settings(settings)
    
    # FilePicker
    def search_button_clicked(self):
        file_path = filedialog.askopenfilename()
        print(file_path)
        if file_path:
            self.settings['file_path'] = file_path
            self.path_label.config(text=self.settings['file_path'])
            col_names = self.controller.get_col_names(self.settings['file_path'])
            # Update response variable optionmenu
            menu = self.response_option['menu']
            menu.delete(0, 'end')
            for name in col_names:
                menu.add_command(label=name, command=lambda value=name: [self.settings['response'].set(value), print(self.settings['response'].get())])
        else:
            raise Exception("No se selecciono ningun archivo")


    def build_button_clicked(self):
        if self.controller is not None:
            self.controller.buildBart(self.settings)