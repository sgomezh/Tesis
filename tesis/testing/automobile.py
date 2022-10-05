# importing required libraries
import dowhy
from dowhy import CausalModel
import pandas as pd
import numpy as np
data = pd.read_csv("D:/Descargas/automobile.csv")

# Imprimir nombres de columnbas
print(data.columns)

data = data.astype({"treatment":'bool'}, copy=False)


# Create a causal model from the data and given common causes.
model=CausalModel(
        data = data,
        treatment='curb_weight',
        outcome='log_price',
        common_causes=["x"+str(i) for  i in range(1,26)]
        )
model.view_model()
from IPython.display import Image, display
display(Image(filename="causal_model.png"))

#Identify the causal effect
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
'''print(identified_estimand)'''

# Estimate the causal effect and compare it with Average Treatment Effect
estimate = model.estimate_effect(identified_estimand,
        method_name="backdoor.linear_regression", test_significance=True
)

#print(estimate)

print("Causal Estimate is " + str(estimate.value))
data_1 = data[data["treatment"]==1]
print(data_1)
data_0 = data[data["treatment"]==0]
print(data_0)
print("ATE", np.mean(data_1["y_factual"])- np.mean(data_0["y_factual"]))
# Refute the obtained estimate using a placebo test
refute_results=model.refute_estimate(identified_estimand, estimate,
        method_name="random_common_cause")
print(refute_results)