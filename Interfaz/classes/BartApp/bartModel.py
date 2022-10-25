# En este archivo se encuentra el modelo de los datos necesarios para correr el BART

class bartModel:
    def __init__(self):
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
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self._settings = settings

    @property
    def bart(self):
        return self._bart

    @bart.setter
    def bart(self, bart):
        self._bart = bart