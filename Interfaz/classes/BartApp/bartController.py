# En este archivo se encuentran los controladores de la vista de BART

class bartController:
    def __init__(self, model, view, parent):
        self.model = model
        self.view = view
        self.parent = parent

    # Construye el modelo de BART
    def buildBart(self):
        import bartMethods.buildBart as bb

        self.model.bart = bb.buildBartModelV2(self.model.settings)

    # Almacena la confirugarion en el modelo
    def store_settings(self, settings):
        # Iterate over settings map
        for key, value in settings.items():
            if(type(value) == str):
                self.model.settings[key] = value
            else:
                self.model.settings[key] = value.get()
            


    # Obtiene las columnas del dataset
    def get_col_names(self, path):
        import pandas as pd
        dataset = pd.read_csv(path)
        return list(dataset.columns)