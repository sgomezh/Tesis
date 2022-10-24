# En este archivo se encuentran los controladores de la vista de BART

class bartController:
    def __init__(self, model, view, parent):
        self.model = model
        self.view = view
        self.parent = parent

    # Construye el modelo de BART
    def buildBart(self):
        import bartMethods.buildBart as bb
        self.model.settings = self.view.settings
        self.model.bart = bb.buildBartModelV2(self.model.settings)

    # Almacena la confirugarion en el modelo
    def store_settings(self, settings):
        for key in settings:
            self.model.settings[key] = settings[key]

    # Obtiene las columnas del dataset
    def get_col_names(self, path):
        import pandas as pd
        dataset = pd.read_csv(path)
        return list(dataset.columns)