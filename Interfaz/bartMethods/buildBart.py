from tkinter import filedialog, Label, Entry, Button, Text
from tkinter.font import Font
from rpy2.robjects import r, FloatVector
from rpy2.robjects.packages import importr

def buildBartModelV2(settings):
    # Se utilizara 0.8 de los datos para entrenamiento y 0.2 para test
    import pandas as pd
    from numpy.random import rand
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.packages import importr
    from rpy2.robjects import r 
    import numpy as np

    pandas2ri.activate()
    df = pd.read_csv(settings['file_path'])

    # Si hay tratamiento, se convierte la columna a boolean
    if settings['treatment'] != 'None':
        df[settings['treatment']] = df[settings['treatment']].astype(bool)

    msk = rand(len(df)) < 0.8
    # Split data into train and test
    train = df[msk]
    test = df[~msk]
    
    mh_values = normalizeValues(settings['grow'], settings['prune'], settings['change'])

    bPackage = importr('bartMachine')


    


    if settings['cv']:
        # TODO: Poner una pantalla de carga para esta funcion
        bart = bPackage.build_bart_machine_cv(X = train.loc[: , train.columns != settings['response']],
                                                y = train.loc[:, settings['response']])
    else:
        bart = bPackage.build_bart_machine(X = train.loc[: , train.columns != settings['response']],
                                            y = train.loc[:, settings['response']],
                                            num_trees = settings['n_trees'],
                                            num_burn_in = settings['burn_in_iter'],
                                            num_iterations_after_burn_in = settings['after_burn_in_iter'],
                                            alpha = settings['alpha'],
                                            beta = float(settings['beta']),
                                            k = float(settings['k']),
                                            q = float(settings['q']),
                                            nu = float(settings['nu']),
                                            mh_prob_steps = FloatVector(mh_values)
                                            )

    r.assign('bart', bart)

    r('summ <- capture.output(summary(bart))')

    summary = np.array(r['summ'])
    oos_perf = bPackage.bart_predict_for_test_data(bart, test.loc[: , test.columns != settings['response']], test.loc[:, settings['response']])

    r.assign('oos_perf', oos_perf)
    r('nameList <- names(oos_perf)')
    
    nameList = r('nameList')

    displayText = summary.tolist()
    displayText.append("Out of sample performance:")

    for i in range(len(oos_perf)):
        if(nameList[i] == 'e' or nameList[i] == 'y_hat'):
            continue

        displayText.append(nameList[i] + ": " + str(oos_perf[i]))
    displayText.append("")

                              
    return bart, displayText
    

# Convierte los valores de los porcentajes a valores entre 0 y 1
def normalizeValues(grow, prune, change):
    # Creamos una constante normalizadora
    normalizer = 1 / (grow + prune + change)
    grow = grow * normalizer
    prune = prune * normalizer
    change = change * normalizer
    return [grow, prune, change]

def predict_with_bart(bart, df):
    # TODO: Revisar este metodo
    from rpy2.robjects import pandas2ri
    from rpy2.robjects import r
    import pandas as pd
    pandas2ri.activate()

    df = pd.read_csv(df, header=0)

    bPackage = importr('bartMachine')
    pred = bPackage.predict_bartMachine(bart, df)

    r.assign('pred', pred)
    r('''
        save_path <- './Predicciones/predicciones.csv'
        write.csv(pred, file = save_path)
    ''')
    save_path = r('save_path')
    summary = r('summary(pred)')
    nameList = r('names(summary(pred))')
    print(nameList)


    displayText = ["Predicciones guardadas en: " + save_path[0]]
    return displayText



def display_var_importance(bart):
    from rpy2.robjects.packages import importr
    bPackage = importr('bartMachine')
    path = 'var_importance.png'
    # Use png() to save the plot to a file
    r['png'](path)
    bPackage.investigate_var_importance(bart)
    r['dev.off']()
    return path
    
def calculateATE(bart, settings):

    if settings['treatment'] == 'None':
        raise Exception('No se ha seleccionado un tratamiento')
        
    else: 
        import pandas as pd
        from rpy2.robjects.packages import importr
        from rpy2.robjects import pandas2ri
        pandas2ri.activate()


        r.assign('bart', bart)
        
        # Cast treatment to float
        r.assign('treatment', settings['treatment'])
        
        
        r('''
            library(bartMachine)
            library(tidytreatment)

            ate <- avg_treatment_effects(bart, treatment)

            r_value = ate$ate[1000]
        ''')
        ate = r('r_value')

        displayText = ["Estimated ATE for " + settings['treatment'] + ": " + str(ate)]
    return ate, displayText
        
        
