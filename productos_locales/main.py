
#%%

# Importación de librerías #
################s############

# Importar librerías para tratamiento de datos
# --------------------------------------------
import pandas as pd 

# Importar scripts
# ----------------
from src import idiazabal as i 

# Extracción de datos #
#######################
lista_idiazabal = i.extraer_idiazabal()

# Limpieza #
############

df_idiazabal = i.limpiar_idiazabal(lista_idiazabal)

# %%
