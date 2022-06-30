from dowhy import CausalModel
import dowhy
import dowhy.datasets
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
data = dowhy.datasets.linear_dataset(
    beta=10,
    num_common_causes=5,
    num_instruments=2,
    num_samples=10000,
    treatment_is_binary=True)
model = CausalModel(
    data=data["df"],
    treatment=data["treatment_name"],
    outcome=data["outcome_name"],
    graph=data["gml_graph"])

identified_estimand= model.identify_effect(proceed_when_unidentifiable=False)
print(identified_estimand)

dml_estimate = model.estimate_effect(identified_estimand, method_name="backdoor.econml.orf.DMLOrthoForest",
                control_value = 0,
                treatment_value = 1,
                target_units = lambda df: df["X0"]>1,
                confidence_intervals=False,
                method_params={
                    "init_params":{'model_y':GradientBoostingRegressor(),
                                   'model_t': GradientBoostingRegressor(),
                                   'model_final':LassoCV(),
                                   'featurizer':PolynomialFeatures(degree=1, include_bias=True)},
                    "fit_params":{}}
                                        )
print("========================== PASO 4 ==========================")
#=============================================================
refute_results = model.refute_estimate(identified_estimand, dml_estimate,
                                       method_name="random_common_cause")
print(refute_results)