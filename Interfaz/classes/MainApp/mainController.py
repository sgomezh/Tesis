from classes.viewClass import BartApp

# Esta clase se encarga de comunicar la vista y el modelo
class mainController:
    def __init__(self, model, view):
        self._model = model
        self._view = view


    def build_bart_button_clicked(self):
        app = BartApp(self._view)