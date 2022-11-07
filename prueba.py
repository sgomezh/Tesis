

# # importing required libraries
# import dowhy
# from dowhy import CausalModel
# import pandas as pd
# import numpy as np

# data= pd.read_csv("https://raw.githubusercontent.com/AMLab-Amsterdam/CEVAE/master/datasets/IHDP/csv/ihdp_npci_1.csv", header = None)
# col =  ["treatment", "y_factual", "y_cfactual", "mu0", "mu1" ,]
# for i in range(1,26):
#     col.append("x"+str(i))
# data.columns = col
# data = data.astype({"treatment":'bool'}, copy=False)
# model=CausalModel(
#         data = data,
#         treatment='treatment',
#         outcome='y_factual',
#         common_causes=["x"+str(i) for  i in range(1,26)]
#         )



# #Identify the causal effect
# identified_estimand = model.identify_effect(proceed_when_unidentifiable=True, method_name="maximal-adjustment")
# print(identified_estimand)


# # Estimate the causal effect and compare it with Average Treatment Effect
# estimate = model.estimate_effect(identified_estimand,
#         method_name="backdoor.propensity_score_stratification", method_params={'num_strata':50, 'clipping_threshold':5}
# )
# print(estimate)

# print("Causal Estimate is " + str(estimate.value))
# data_1 = data[data["treatment"]==1]
# data_0 = data[data["treatment"]==0]

# print("ATE", np.mean(data_1["y_factual"])- np.mean(data_0["y_factual"]))

common_causes=["x"+str(i) for  i in range(1,26)]
print(common_causes)