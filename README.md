# **Tesis**
Importante leer este documento antes de correr el código. Este repositorio consta de 4 partes fundamentales:

> ### 1. Archivos para correr los métodos de DoWhy
>> #### PARA CORRER **Dowhy**:
>>> 1. Ir a carpeta **"tesis"**
>>> 2. Ir a carpeta **"testing"**                      
>>> 3. Correr:
  >>>> - dowhy_dataset.py, dowhy_linear_regression.py, dowhy_score_matching.py o dowhy_score_weighting.py
  
> ### 2. Archivo para correr el método de EconML
>> #### PARA CORRER **EconML**:
>>> 1. Ir a carpeta **"tesis"**
>>> 2. Ir a carpeta **"testing"**
>>> 3. Correr:
  >>>> - econml_dml.py

> ### 3. Archivo para correr BART
>> #### PARA CORRER **BART**
>>> 1. Ir a carpeta **"tesis"**
>>> 2. Correr:
  >>>> - bart_testing.py

> ### 4. Archivo para correr BART y DoWhy en un mismo bloque de código (y con un mismo dataset) (falta por implementar**)
>>#### PARA CORRER **DoWhy y BART**: (falta por implementar**)
>>> 1. Ir a carpeta **"tesis"**                  
>>> 2. Correr:
<<<<<<< HEAD
  >>>> - DoWhy_BART.py (falta por implementar**)
=======
  >>>> - main.py (falta por implementar**)
>>>>>>> 29ce7f21f61a6079e3f9c73ab5bb5ff32524cff4


### CONFIGURACIÓN DEL DATASET
La configuración del dataset generado por DoWhy (que ocuparemos para tanto para DoWhy, EconML y BART) no necesita una configuración especial para DoWhy y EconML. <br />
**Sin embargo**, si existirán problemas si no se utiliza una configuración especial para correr **BART**. <br />
Para esto:
> 1. Acceder a la carpeta "tesis"
> 2. Acceder a la carpeta "testing"
> 3. Entrar al archivo "dowhy_dataset.py"
> 4. Entre las lineas 26 y 32 se encontrarán los parámetros que crearán el dataset
> 5. La suma entre el parámetro **NUM_COMMON_CAUSES** y **NUM_INSTRUMENTS** deben **SUMAR** **(NUM_SAMPLES - 1)**
<<<<<<< HEAD
> Ejemplo: si **NUM_SAMPLES** es 10, entonces la suma entre **NUM_COMMON_CAUSES** y **NUM_INSTRUMENTS** deben sumar: 10 - 1 = 9 (cualquier número sirve mientras cumpla la regla de la suma). Esto es para no tener problemas de la cuadratura de dimensiones de los arreglos para correr **BART.**
=======
> Ejemplo: si **NUM_SAMPLES** es 10, entonces la suma entre **NUM_COMMON_CAUSES** y **NUM_INSTRUMENTS** deben sumar: 10 - 1 = 9 (cualquier número sirve mientras cumpla la regla de la suma). Esto es para no tener problemas de la cuadratura de dimensiones de los arreglos para correr **BART.**
>>>>>>> 29ce7f21f61a6079e3f9c73ab5bb5ff32524cff4
