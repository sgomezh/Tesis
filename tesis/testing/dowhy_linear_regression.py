#--------------------- Librerías importadas ---------------------
# I. Create a causal model from the data and given graph.
from dowhy import CausalModel
import dowhy.datasets
import warnings
from sklearn.exceptions import DataConversionWarning
import sys
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
from IPython.display import Image, display

#--------------------- Configuraciones de Encoder ---------------------
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
#--------------------- Ignorar warnings ---------------------
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=FutureWarning)
#========================== PASO 1 ==========================
# Crear un modelo causal desde un set de datos y un grafo dado 
#=============================================================
# Cargar una muestra del dataset creado
print("========================== PASO 1 ==========================")
data = dowhy.datasets.linear_dataset(
    beta=10,
    num_common_causes=5,
    num_instruments=2,
    num_samples=10000,
    treatment_is_binary=True)
# Crear el modelo causal
model = CausalModel(
    data=data["df"],
    treatment=data["treatment_name"],
    outcome=data["outcome_name"],
    graph=data["gml_graph"])
# Visualizar el modelo creado y guardar una imagen de este
model.view_model()
display(Image(filename="causal_model.png"))
#========================== PASO 2 ==========================
# Identificar un efecto causal y retornar la estimación objetivo 
#=============================================================
print("========================== PASO 2 ==========================")
identified_estimand= model.identify_effect(proceed_when_unidentifiable=True)
print(identified_estimand)
#========================== PASO 3 ==========================
# Estimar la estimación objetivo usando un método estadistico
#=============================================================
print("========================== PASO 3 ==========================")
estimate = model.estimate_effect(identified_estimand,
                                method_name="backdoor.linear_regression")    
print(estimate)
#========================== PASO 4 ==========================
# Refutar la estimación obtenida
#=============================================================
# Esta refutación se basa en agregar una causa común random o
# factor de consfusion. La estimación no debería verse afectada.
print("========================== PASO 4 ==========================")
#=============================================================
refute_results = model.refute_estimate(identified_estimand, estimate,
                                       method_name="random_common_cause")
print(refute_results)
