from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
import sys
import warnings
from sklearn.exceptions import DataConversionWarning
from classes.MainApp.appModel import appModel

def estimate_effect():

    #--------------------- Configuraciones de Encoder ---------------------
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    #--------------------- Ignorar warnings ---------------------
    warnings.filterwarnings(action='ignore', category=DataConversionWarning)
    warnings.filterwarnings(action='ignore', category=FutureWarning)

    model = appModel.getDowhyModel()
    #Identify the causal effect
  
    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

    appModel.setDowhyIdentifiedEstimand(identified_estimand)
    settings = appModel.getDowhySettings()

    '''print(identified_estimand)'''
    if settings['estimation_option'] == '0':
        # Estimate the causal effect and compare it with Average Treatment Effect
        estimate = model.estimate_effect(identified_estimand,
                method_name="backdoor.linear_regression")
        print('linear_regression')
            
    elif settings['estimation_option'] == '1':
        estimate = model.estimate_effect(identified_estimand,
                method_name="backdoor.propensity_score_matching")
        print('propensity_score_matching')
        
    elif settings['estimation_option'] == '2':
        estimate = model.estimate_effect(identified_estimand,
                method_name="backdoor.propensity_score_weighting")
        print('propensity_score_weighting')

    elif settings['estimation_option'] == '3':
        estimate = model.estimate_effect(identified_estimand, 
                method_name="backdoor.econml.dml.DML",
                                     control_value = 0,
                                     treatment_value = 1,
                                 target_units = lambda df: df["X0"]>1,  # condition used for CATE
                                 confidence_intervals=False,
                                method_params={"init_params":{'model_y':GradientBoostingRegressor(),
                                                              'model_t': GradientBoostingRegressor(),
                                                              "model_final":LassoCV(fit_intercept=False), 
                                                              'featurizer':PolynomialFeatures(degree=1, include_bias=False)},
                                               "fit_params":{}})
        print('dml')
    print("Causal Estimate is " + str(estimate.value))
    

