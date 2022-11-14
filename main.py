from classes.MainApp.appController import appController
from classes.MainApp.appModel import appModel
from views.mainView import mainView

# ----------------------- Inicializacion de la ventana principal ----------------------

def main():
    view = mainView()
    model = appModel()
    controller = appController(model, view)
    view.setController(controller)
    view.mainloop() 


if __name__ == '__main__':
    main()