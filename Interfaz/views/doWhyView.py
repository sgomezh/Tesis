import classes.viewClass as vc
from tkinter import *
from tkinter import filedialog, OptionMenu, scrolledtext
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import Toplevel
from classes.MainApp import appController 

class DoWhyView(Toplevel):
    def __init__(self, parent, width, height):
        super(DoWhyView, self).__init__(parent)
        self.doWhySettings = {}
        self.iv_list = []
        self.cc_list = []
        self.iv_var = []
        self.cc_var = []
        # --------- Coordenadas de los widgets --------- #
        trt_coordinates = {"x": 10, "y": 215}
        out_coordinates = {"x": 360, "y": 215}
        iv_coordinates = {"x": 100, "y": 260}
        cc_coordinates = {"x": 465, "y": 260}


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

        # --------- Configuracion de los datos del dataset ------------
        self.build_causal_model_label = Label(self, text="Build Causal Model", font=self.title_font, bg='#08013D', fg='#FFFFFF')
        self.build_causal_model_label.place(x=250, y=20)

        self.dataset_label= Label(self, text="Dataset path (csv, txt):", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.dataset_label.place(x=10, y=70)

        self.path_label = Label(self, text="", font=self.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
        self.path_label.place(x=5, y=100)

        self.search_button = Button(self, text="Search", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: self.search_button_clicked())
        self.search_button.place(x=670, y=95)
        
        self.estimation_method_label= Label(self, text="Effect estimation method:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.estimation_method_label.place(x=10, y=150)

        # --------- Configuracion de los metodos de estimacion ------------
        self.doWhySettings['estimation_option'] = IntVar()
        self.linear_regression_option = Radiobutton(self, text="Linear Regression", font=self.label_font, bg='#08013D', fg='#FFFFFF',padx = 20, variable=self.doWhySettings['estimation_option'], value=0, selectcolor="black")
        self.linear_regression_option.place(x=0, y=180)

        self.score_matching_option = Radiobutton(self, text="Score Matching", font=self.label_font, bg='#08013D', fg='#FFFFFF', variable=self.doWhySettings['estimation_option'], value=1, selectcolor="black")
        self.score_matching_option.place(x=200, y=180)

        self.score_weighting_option = Radiobutton(self, text="Score Weighting", font=self.label_font, bg='#08013D', fg='#FFFFFF', variable=self.doWhySettings['estimation_option'], value=2, selectcolor="black")
        self.score_weighting_option.place(x=400, y=180)

        self.DML_option = Radiobutton(self, text="DML", font=self.label_font, bg='#08013D', fg='#FFFFFF', variable=self.doWhySettings['estimation_option'], value=3, selectcolor="black")
        self.DML_option.place(x=600, y=180)

        # --------- Treatment column ------------
        self.treatment_column_label= Label(self, text="Treatment column:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.treatment_column_label.place(x=trt_coordinates['x'], y=trt_coordinates['y'])
        
        self.doWhySettings['treatment_column'] = StringVar()
        self.treatment_column_menu = OptionMenu(self, self.doWhySettings['treatment_column'], "")
        self.treatment_column_menu.config(font=self.label_font, bg='#FFFFFF', fg='#000000', width=15, height=1)
        self.treatment_column_menu.place(x=trt_coordinates['x']+160, y=trt_coordinates['y'])

        # --------- Outcome column ------------
        self.outcome_column_label= Label(self, text="Outcome column:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.outcome_column_label.place(x=out_coordinates['x'], y=out_coordinates['y'])

        self.doWhySettings['outcome_column'] = StringVar()
        self.outcome_column_menu = OptionMenu(self, self.doWhySettings['outcome_column'], "")
        self.outcome_column_menu.config(font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, height=1)
        self.outcome_column_menu.place(x=out_coordinates["x"]+160, y=out_coordinates["y"])
        
        # --------- Instrument column ------------
        self.intrumental_variables_label= Label(self, text="Instrumental Variables", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.intrumental_variables_label.place(x=iv_coordinates['x'], y=iv_coordinates['y'])

        self.iv_scrolltext = scrolledtext.ScrolledText(self, width=30, height=13, font=self.label_font, bg='#FFFFFF', fg='#000000')
        self.iv_scrolltext.place(x=iv_coordinates['x']-60, y=iv_coordinates['y']+30)


        # --------- Common causes column ------------
        self.common_causes_label= Label(self, text="Common Causes", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.common_causes_label.place(x=cc_coordinates["x"]+80, y=cc_coordinates["y"])	

        self.cc_scrolltext = scrolledtext.ScrolledText(self, width=32, height=13, bg='#FFFFFF', font=self.label_font)
        self.cc_scrolltext.place(x=cc_coordinates["x"], y=cc_coordinates["y"]+30)

        # --------- Save button ------------
        self.save_button = Button(self, text="Save", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: self.save_button_clicked())
        self.save_button.place(x=350, y=550)
        
        # --------- Controller ------------
        self.controller = None



    def set_controller(self, controller):
        self.controller = controller

    def search_button_clicked(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.path_label = Label(self, text=file_path, font=self.label_font, bg='#FFFFFF', fg='#000000', width=65, height=1)
            self.path_label.place(x=5, y=100)
            # Guardado en memoria
            self.doWhySettings['file_path'] = file_path

            col_names = self.controller.get_col_names(file_path)
            # Update treatment column menu
            treatment_menu = self.treatment_column_menu["menu"]
            treatment_menu.delete(0, "end")
            outcome_menu = self.outcome_column_menu["menu"]
            outcome_menu.delete(0, "end")

            self.iv_list.clear()
            self.cc_list.clear()
            self.cc_var.clear()
            self.iv_var.clear()
            self.iv_scrolltext.delete('1.0', END)
            self.cc_scrolltext.delete('1.0', END)
            

            for name in col_names:
                treatment_menu.add_command(label=name, command=lambda value=name: self.doWhySettings['treatment_column'].set(value))
                outcome_menu.add_command(label=name, command=lambda value=name: [self.doWhySettings['outcome_column'].set(value)])

                var = IntVar(value = 0)
                self.iv_list.append(Checkbutton(self, text=name, variable=var, onvalue=1, offvalue=0, width=20, height=1, padx=5, pady=5, font=self.label_font))
                self.iv_scrolltext.window_create("end", window=self.iv_list[-1])
                self.iv_var.append(var)

                var = IntVar(value = 0)
                self.cc_list.append(Checkbutton(self, text=name, variable=var, onvalue=1, offvalue=0, width=20, height=1, padx=5, pady=5, font=self.label_font))
                self.cc_scrolltext.window_create("end", window=self.cc_list[-1])
                self.cc_var.append(var)

        else:
            import views.alertWindows as aw
            aw.datasetError()
            
    
    
    def save_button_clicked(self):
        # We store the selected checkboxes in a list
        self.doWhySettings['instrumental_variables'] = []
        self.doWhySettings['common_causes'] = []
        for i in range(len(self.iv_var)):
            if self.iv_var[i].get() == 1:
                self.doWhySettings['instrumental_variables'].append(self.iv_list[i]['text'])

            if self.cc_var[i].get() == 1:
                self.doWhySettings['common_causes'].append(self.cc_list[i]['text'])

        # Se guarda la configuracion
        self.controller.store_doWhySettings(self.doWhySettings)
        # Se crea el modelo de dowhy
        self.controller.buildDoWhy()
        # Se cierra la ventana
        self.destroy()
        # Se escribe un mensaje por pantalla
        display_text = "Causal model created successfully."
        self.controller.update_text(display_text.split("\n")) 


    # Guarda la configuracion de dowhy
    def saveSettingsDowhy(self, settings):
        for key, value in settings.items():
            if type(value) == str:
                self.doWhySettings[key] = value
            else:
                self.doWhySettings[key] = value.get()
                
        


    
        