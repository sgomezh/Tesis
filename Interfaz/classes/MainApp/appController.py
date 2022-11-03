from views.bartView import PredictView
from classes.viewClass import BartApp, DoWhyApp, PredictApp
from dowhyMethods.estimate import estimate_effect


# Este es el controlador principal de la aplicacion
class appController:
    def __init__(self, model, mainView):
        self._model = model
        self._mainView = mainView
        self._controller = self

    # Getters
    @property
    def model(self):
        return self._model
    
    @property
    def mainView(self):
        return self._mainView

    @property
    def controller(self):
        return self._controller

# VISTAS
# ---------------- Inicio: Botones del Main ------------------------------
    
# --------------------- BART ---------------------    
    def build_bart_button_clicked(self):
        self.bartApp = BartApp(self)

    def predict_button_clicked(self):
        if (self.model.bartInstance is not None):
            self.predictApp = PredictApp(self)
        else:
            import views.alertWindows as aw
            aw.bartModelError()
            raise Exception("No se ha construido el modelo BART")
            
        
    def variable_importance_button_clicked(self):
        if (self.model.bartInstance is not None):
            from bartMethods.buildBart import display_var_importance
            image_path = display_var_importance(self.model.bartInstance)
            # AQUI VA EL CODIGO PARA MOSTRAR LA IMAGEN, LA RUTA ES Instance/var_importance.png
            self.mainView.update_image(image_path)

        else:
            import views.alertWindows as aw
            aw.bartModelError()
            raise Exception("No se ha construido el modelo BART")
            

    def ate_button_clicked(self):
        pass
# --------------------- DOWHY ---------------------
    def causal_model_button_clicked(self):
        self.dowhyApp = DoWhyApp(self)

    def causal_graph_button_clicked(self):
        if (self.model.dowhyModel is not None):
            from dowhyMethods.causalGraph import generateCausalGraph
            img_path = generateCausalGraph(self.model.dowhyModel)
            self.mainView.update_image(img_path)
        else:
            import views.alertWindows as aw
            aw.dowhyModelError()
            raise Exception("No se ha construido el modelo de DoWhy")
            

    def estimate_effect_button_clicked(self):
        from dowhyMethods.estimate import estimate_effect
        if (self.model.dowhyModel and self.model.doWhySettings is not None):
            self.model.dowhyIdentifiedEstimand, self.model.doWhyEstimate, displayText = estimate_effect(self.model.dowhyModel, self.model.doWhySettings)
            self.mainView.update_text(displayText)
        else:
            import views.alertWindows as aw
            aw.estimateError()
            raise Exception("No se ha construido el modelo de DoWhy")

    def refute_button_clicked(self):
        from dowhyMethods.refute import refute
        if (self.model.dowhyModel and self.model.dowhyIdentifiedEstimand and self.model.doWhyEstimate is not None):
            displayText = refute(self.model.dowhyModel, self.model.dowhyIdentifiedEstimand, self.model.doWhyEstimate)
            self.mainView.update_text(displayText)
        else:
            import views.alertWindows as aw
            aw.refuteError()
            raise Exception("No se ha construido el modelo de DoWhy")

# ---------------- Termino: Botones del Main ------------------------------


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# FUNCIONES
    # Construye el modelo de BART
    def buildBart(self):
        import bartMethods.buildBart as bb
        self.model.bartInstance, bartInfo = bb.buildBartModelV2(self.model.bartSettings)
        # Formatea el texto a mostrar
        displayText = bartInfo[0].tolist()

        self.mainView.update_text(displayText)
        
    def buildDoWhy(self):
        from dowhyMethods.buildCausalModel import generateCausalModel
        self.model.dowhyModel = generateCausalModel(self.model.doWhySettings)

    # Almacena la configuracion en el modelo
    def store_bartSettings(self, settings):
        # Iterate over settings map
        for key, value in settings.items():
            if(type(value) == str):
                self.model.bartSettings[key] = value
            else:
                self.model.bartSettings[key] = value.get()


    # Obtiene las columnas del dataset
    def get_col_names(self, path):
        import pandas as pd
        dataset = pd.read_csv(path)
        return list(dataset.columns)


    def predictBart(self, dataPath):
        from bartMethods.buildBart import predict_with_bart
        text = predict_with_bart(self.model.bartInstance, dataPath)
        self.mainView.update_text(text)
    
    
    def store_doWhySettings(self, settings):
        for key, value in settings.items():
            if type(value) == str:
                self.model.doWhySettings[key] = value
            else:
                self.model.doWhySettings[key] = str(value.get()).split(",")
                if len(self.model.doWhySettings[key]) == 1:
                    self.model.doWhySettings[key] = self.model.doWhySettings[key][0]


    def on_closing(self):
        self.model = None
        # delattr(self.model, "_doWhyModel")
        self.mainView.destroy()

    def update_text(self, text):
        self.mainView.update_text(text)