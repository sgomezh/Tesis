import dowhy
from dowhy import CausalModel
import pandas as pd
import numpy as np


data= pd.read_csv("automobile.csv")

names = list(data.columns)

names.remove('curb_weight')
names.remove('log_price')

# Create a causal model from the data and given common causes.
model=CausalModel(
        data = data,
        treatment='curb_weight',
        outcome='log_price',
        common_causes=names
        )
model.view_model()
from IPython.display import Image, display
display(Image(filename="causal_model.png"))

#Identify the causal effect
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True, method_name="maximal-adjustment")
print(identified_estimand)

# Estimate the causal effect and compare it with Average Treatment Effect
estimate = model.estimate_effect(identified_estimand,
    method_name="backdoor.linear_regression"
)

print("Causal Estimate is " + str(estimate.value))

data_1 = data[data["treatment"]==1]
data_0 = data[data["treatment"]==0]

print("ATE", np.mean(data_1["y_factual"])- np.mean(data_0["y_factual"]))

