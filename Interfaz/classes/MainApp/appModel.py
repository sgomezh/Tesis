# Aqui se manejan todos los datos del modelo
class appModel:
    def __init__(self):
        self._bartSettings = {
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
        self._bartInstance = None
        self._doWhySettings = {}
        self._doWhyInstance = None

    @property
    def bartSettings(self):
        return self._bartSettings

    @bartSettings.setter
    def bartSettings(self, settings):
        self._bartSettings = settings

    @property
    def bartInstance(self):
        return self._bartInstance

    @bartInstance.setter
    def bartInstance(self, bart):
        self._bartInstance = bart
        
    @property
    def doWhySettings(self):
        return self._doWhySettings

    @doWhySettings.setter
    def doWhySettings(self, settings):
        self._doWhySettings = settings  