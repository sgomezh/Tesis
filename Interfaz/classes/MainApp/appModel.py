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
        self._dowhyIdentifiedEstimand = None
        self._doWhyModel = None
        self._doWhyEstimate = None
        self._doWhyRefute = None
        self._appText = None

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

    @property
    def dowhyModel(self):
        return self._doWhyModel
    
    @dowhyModel.setter
    def dowhyModel(self, model):
        self._doWhyModel = model

    @property
    def dowhyIdentifiedEstimand(self):
        return self._dowhyIdentifiedEstimand

    @dowhyIdentifiedEstimand.setter
    def dowhyIdentifiedEstimand(self, identified_estimand):
        self._dowhyIdentifiedEstimand = identified_estimand
    
    @property
    def dowhyEstimate(self):
        return self._doWhyEstimate
    
    @dowhyEstimate.setter    
    def dowhyEstimate(self, estimate):
        self._doWhyEstimate = estimate
    
    @property
    def dowhyRefute(self):
        return self._doWhyRefute
    
    @dowhyRefute.setter
    def dowhyRefute(self, refute):
        self._doWhyRefute = refute

    @property
    def causalGraph(self):
        return self._causalGraph

    @causalGraph.setter
    def causalGraph(self, graph):
        self._causalGraph = graph

    @property
    def appText(self):
        return self._appText
    
    @appText.setter
    def appText(self, text):
        self._appText = text
    