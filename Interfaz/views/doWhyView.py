import classes.viewClass as vc
from tkinter import *
from tkinter import filedialog, OptionMenu
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import Toplevel
from classes.MainApp.appModel import appModel

class DoWhyView(Toplevel):
    def __init__(self, parent, width, height):
        super(DoWhyView, self).__init__(parent)
        self.doWhySettings = {}

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
        self.treatment_column_label.place(x=10, y=250)
        
        self.doWhySettings['treatment_column'] = StringVar()
        self.treatment_column_menu = OptionMenu(self, self.doWhySettings['treatment_column'], "")
        self.treatment_column_menu.config(font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, height=1)
        self.treatment_column_menu.place(x=200, y=250)

        # --------- Outcome column ------------
        self.outcome_column_label= Label(self, text="Outcome column:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.outcome_column_label.place(x=10, y=300)

        self.doWhySettings['outcome_column'] = StringVar()
        self.outcome_column_menu = OptionMenu(self, self.doWhySettings['outcome_column'], "")
        self.outcome_column_menu.config(font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, height=1)
        self.outcome_column_menu.place(x=200, y=300)
        
        # --------- Instrument column ------------
        self.intrumental_variables_label= Label(self, text="Instrumental Variables:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.intrumental_variables_label.place(x=10, y=350)

        self.doWhySettings['instrumental_var_column'] = StringVar()
        self.intrumental_variables_entry = Entry(self, font=self.label_font, bg='#FFFFFF', fg='#000000', width=20, textvariable=self.doWhySettings['instrumental_var_column'], justify='left')
        self.intrumental_variables_entry.place(x=200, y=350)

        # --------- Common causes column ------------
        self.common_causes_label= Label(self, text="Common Causes:", font=self.label_font, bg='#08013D', fg='#FFFFFF')
        self.common_causes_label.place(x=10, y=400)

        self.doWhySettings['common_causes_column'] = StringVar()
        self.common_causes_entry = Entry(self, font=self.label_font, bg='#FFFFFF', fg='#000000', textvariable=self.doWhySettings['common_causes_column'], width=20, justify='left')
        self.common_causes_entry.place(x=200, y=400)

        # --------- Save button ------------
        self.save_button = Button(self, text="Save", font=self.button_font, bg='#FFFFFF', fg='#000000', width=10, height=1, command= lambda: [self.saveSettingsDowhy(self.doWhySettings), self.destroy()])
        self.save_button.place(x=350, y=450)
        
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
            # Guardado en txt
            f = open ('dowhy_dataset.txt','w')
            f.write(file_path)
            f.close()

            col_names = self.controller.get_col_names(file_path)
            # Update treatment column menu
            menu = self.treatment_column_menu["menu"]
            menu.delete(0, "end")
            for name in col_names:
                menu.add_command(label=name, command=lambda value=name: [self.doWhySettings['treatment_column'].set(value), print(self.doWhySettings['treatment_column'].get())])
            # Update outcome column menu
            menu = self.outcome_column_menu["menu"]
            menu.delete(0, "end")
            for name in col_names:
                menu.add_command(label=name, command=lambda value=name: [self.doWhySettings['outcome_column'].set(value), print(self.doWhySettings['outcome_column'].get())])
        else:
            raise Exception("No se ha seleccionado ningun archivo.")
        
    def save_button_clicked(self):
        self.controller.store_doWhySettings(self.doWhySettings)
        self.controller.buildDoWhy()
        self.destroy()

    def saveSettingsDowhy(self, settings):
        for key, value in settings.items():
            if type(value) == str:
                self.doWhySettings[key] = value
            else:
                self.doWhySettings[key] = value.get()
        dict = self.doWhySettings
        appModel.setDoWhySettings(dict)

    '''def splitVariables(setting_list):
        setting_list = setting_list.split(",")
        if len(setting_list) == 1:
            setting_list = setting_list[0]
        return setting_list
    
    def getDowhySettinngs(): 
        settings = {} 
        setting_list = []
        file = open ('dowhy_settings.txt','r')
        for line in file:
            c = '\n'
            new_line = line.replace(c,"")
            setting_list.append(new_line)
        for i in range(len(setting_list)):
            if i == 0:
                settings['estimation_option'] = splitVariables(setting_list[i])
            elif i == 1:
                settings['treatment_column'] = splitVariables(setting_list[i])
            elif i == 2:
                settings['outcome_column'] = splitVariables(setting_list[i])
            elif i == 3:
                settings['instrumental_variables'] = splitVariables(setting_list[i])
            elif i == 4:
                settings['common_causes'] = splitVariables(setting_list[i])
        return settings
'''
    
        