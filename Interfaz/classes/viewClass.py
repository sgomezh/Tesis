from views.bartView import BartView, PredictView
from views.doWhyView import DoWhyView

class BartApp():
    def __init__(self, parent):
        super().__init__()
        # Coordenadas de los widgets
        self.model = parent.model
        self.view = BartView(parent.mainView, self.model.bartSettings, 800, 600)
        self.controller = parent.controller

        self.view.set_controller(self.controller)

    def close(self):
        self.view.destroy()


class PredictApp():
    def __init__(self, parent):
        super().__init__()
        self.model = parent.model
        self.view = PredictView(parent.mainView)
        self.controller = parent.controller

        self.view.set_controller(self.controller)
    


class DoWhyApp:
    def __init__(self, parent):
        self.model = parent.model
        self.view = DoWhyView(parent.mainView, 800, 600)
        self.controller = parent.controller
        
        self.view.set_controller(self.controller)

