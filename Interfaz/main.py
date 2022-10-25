from classes.MainApp.mainController import mainController
from classes.MainApp.mainModel import mainModel
from classes.MainApp.mainView import mainView

# ----------------------- Inicializacion de la ventana principal ----------------------

def main():
    rootView = mainView()
    rootModel = mainModel()
    rootController = mainController(rootModel, rootView)

    rootView.setController(rootController)
    
    rootView.mainloop()


if __name__ == '__main__':
    main()