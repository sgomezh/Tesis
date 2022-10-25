
# Esta clase almacena las instancias de BART y DoWhy
class mainModel:
    def __init__(self):
        self._doWhyInstance = None
        self._bartInstance = None

    @property
    def doWhyInstance(self):
        return self._doWhyInstance
    
    @doWhyInstance.setter
    def doWhyInstance(self, doWhyInstance):
        self._doWhyInstance = doWhyInstance
    
    @property
    def bartInstance(self):
        return self._bartInstance
    
    @bartInstance.setter
    def bartInstance(self, bartInstance):
        self._bartInstance = bartInstance