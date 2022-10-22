# En este archivo se encuentran los controladores de la vista de BART

class bartController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    # Construye el modelo de BART
    def buildBart(self):
        import bartMethods.buildBart as bb
        self.model.settings = self.view.settings
        self.bart = bb.buildBartModelV2(self.model.settings)

    # Almacena la confirugarion en el modelo
    def store_settings(self, settings):
        self.model.settings = settings

    # Obtiene las columnas del dataset
    def get_col_names(self, path):
        import pandas as pd
        dataset = pd.read_csv(path)
        return list(dataset.columns)