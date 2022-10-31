import dowhy
from dowhy import CausalModel
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
import sys
import warnings
from sklearn.exceptions import DataConversionWarning
from classes.MainApp.appModel import appModel


def generateCausalGraph():
    model = appModel.getDowhyModel()
    model.view_model()
    from IPython.display import Image, display
    display(Image(filename="causal_model.png"))

