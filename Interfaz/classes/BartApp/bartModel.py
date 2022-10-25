# En este archivo se encuentra el modelo de los datos necesarios para correr el BART

class bartModel:
    def __init__(self):
        self._datasetPath = None
        self._settingsPath = None
        # Dataset y settings se guarda como un dataframe de pandas
        self._dataset = None
        self._bart = None
        self._settings = {
            "response": "",
            "cv": False,
            "n_trees": 200,
            "burn_in_iter": 250,
            "after_burn_in_iter": 1000,
            "alpha": 0.95,
            "beta": 2,
            "k": 2,
            "q": 0.9,
            "nu": 3,
            "grow": 30,
            "prune": 30,
            "change": 40
        }

    @property
    def datasetPath(self):
        return self._datasetPath
    
    @datasetPath.setter
    def datasetPath(self, datasetPath):
        self._datasetPath = datasetPath
    
    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        self._dataset = dataset

    # Funcion para cargar el dataset a partir del path
    def loadDataset(self):
        if self._dataset is None:
            import pandas as pd
            try:
                self._dataset = pd.read_csv(self._datasetPath)
            except:
                raise Exception("Error al cargar el dataset")
    
    # Funcion para retornar los nombres de las columnas del dataset
    def getDatasetColumns(self):
        if self._dataset is not None:
            has_header = not any(cell.isdigit() for cell in self._dataset[0])
            if(not has_header):
                # Create a list of column names as x1, x2, x3, ...
                for i in range(len(self._dataset.columns)):
                    self._dataset.columns[i] = 'x' + str(i)
            return self._dataset.columns
        else:
            raise Exception("No se ha cargado el dataset")

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings

    # Funcion para cargar la configuracion a partir del path
    def loadSettings(self):
        if self._settings is None:
            import pandas as pd
            try:
                # Se asume que tiene header
                self._settings = pd.read_csv(self._settings)
            except:
                raise Exception("Error al cargar la configuracion")

    @property
    def settingsPath(self):
        return self._settingsPath

    @settingsPath.setter
    def settingsPath(self, settingsPath):
        self._settingsPath = settingsPath

    @property
    def bart(self):
        return self._bart

    @bart.setter
    def bart(self, bart):
        self._bart = bart

    def buildBart(self):
        if (self._dataset is not None) and (self._settings is not None):
            import bartMethods.buildBart as BB
            self._bart = BB.buildBartModelV2(self._datasetPath, self._settings)
        else:
            raise Exception("No se ha cargado el dataset o el archivo de configuracion")
            
    
