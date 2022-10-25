from views.bartView import PredictView
from classes.viewClass import BartApp, DoWhyApp

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
    def build_bart_button_clicked(self):
        self.bartApp = BartApp(self)

    def predict_button_clicked(self):
        pred = PredictView(self.mainView)

    def variable_importance_button_clicked(self):
        pass

    def ate_button_clicked(self):
        pass

    def causal_model_button_clicked(self):
        self.dowhyApp = DoWhyApp(self)

    def causal_graph_button_clicked(self):
        pass

    def estimate_effect_button_clicked(self):
        pass

    def refute_button_clicked(self):
        pass

# ---------------- Termino: Botones del Main ------------------------------


# ---------------- Inicio: Botones de la vista BART -----------------------

# ---------------- Termino: Botones de la vista BART ----------------------

# ---------------- Inicio: Botones de la vista DoWhy -----------------------

# ---------------- Termino: Botones de la vista DoWhy ----------------------

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# FUNCIONES
    # Construye el modelo de BART
    def buildBart(self):
        import bartMethods.buildBart as bb
        self.model.bartInstance = bb.buildBartModelV2(self.model.bartSettings)

    # Almacena la confirugarion en el modelo
    def store_settings(self, settings):
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
    
    def predictBart(self, data):
        from bartMethods import predict_with_bart
        predict_with_bart(self.model.bartInstance, data)
    