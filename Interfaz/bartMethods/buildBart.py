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

    pandas2ri.activate()
    df = pd.read_csv(settings['file_path'])
    msk = rand(len(df)) < 0.8
    # Split data into train and test
    train = df[msk]
    test = df[~msk]
    
    mh_values = normalizeValues(settings['grow'], settings['prune'], settings['change'])

    bPackage = importr('bartMachine')

    if settings['cv']:
        # TODO: Poner una pantalla de carga para esta funcion
        bart = bPackage.build_bart_machine_cv(X = df.loc[: , df.columns != settings['response']],
                                                y = df.loc[:, settings['response']])
    else:
        bart = bPackage.build_bart_machine(X = df.loc[: , df.columns != settings['response']],
                                            y = df.loc[:, settings['response']],
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
        

    return bart
    

# Convierte los valores de los porcentajes a valores entre 0 y 1
def normalizeValues(grow, prune, change):
    # Creamos una constante normalizadora
    #mh_values = {}
    normalizer = 1 / (grow + prune + change)
    # Normalizamos los valores
    # mh_values['grow'] = grow * normalizer
    # mh_values['prune'] = prune * normalizer
    # mh_values['change'] = change * normalizer
    grow = grow * normalizer
    prune = prune * normalizer
    change = change * normalizer
    return [grow, prune, change]
    #return mh_values

def predict_with_bart(bart, df):
    from rpy2.robjects import pandas2ri
    from rpy2.robjects import r
    pandas2ri.activate()
    bPackage = importr('bartMachine')
    pred = bPackage.predict_bart_machine(bart, df)

    r['summary'](pred)
    
