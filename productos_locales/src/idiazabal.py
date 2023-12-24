#%%
# Importación de librerías #
############################

# Importar librerías para tratamiento de datos
# --------------------------------------------
import pandas as pd 

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver 


# Importar librerías para pausar la ejecución
# -----------------------------------------------------------------------
from time import sleep 

# Configuraciones
# -----------------------------------------------------------------------
pd.set_option('display.max_columns', None)  # Establece una opción de Pandas para mostrar todas las columnas de un DataFrame.

#%% 

# Extracción de datos #
#######################

def extraer_idiazabal ():
    """
    Esta función extrae los datos de la web de quesosidiazabal.com y los devuelve en una listade listas.
        
    Args:
    Esta función no recibe argumentos

    Returns:
    - lista_datos: lista de listas de cada productos con toda la información recogida de la web (datos, imagen, descripcion, facebook, twitter, google, instagram).
    """

    # Inicializar el navegador Firefox
    driver = webdriver.Firefox()

    # Maximizar la ventana
    driver.maximize_window()

    # Navegar a la web
    driver.get("https://www.quesoidiazabal.eus/productores")

    # Recoger los datos de cada uno de los productores
    lista_datos =[]
    i = 1
    while True:
        try:
            sleep(1)
            # Hacer click en el primer productor:
            driver.find_element("css selector", f"li.col-xs-12:nth-child({i}) > a:nth-child(1)").click()

            # Recoger los datos principales del productor en una sola string
            datos = driver.find_element('css selector', '.producer-data-txt').text

            # Guardar la url de la imagen        
            imagen = driver.find_element("css selector", ".center-block").get_attribute("src")
            
            # Descripción
            try:
                descripcion = driver.find_element('css selector', 'div.row:nth-child(4) > div:nth-child(1)').text
            except:
                descripcion = "No disponible"
            
            # Redes sociales             
                ## Facebook  
            try:
                facebook = driver.find_element("css selector", ".facebook").get_attribute("href") 
            except:
                facebook = "No disponible"

                ## Twitter
            try:
                twitter = driver.find_element("css selector", ".twitter").get_attribute("href") 
            except:
                twitter = "No disponible"    
                
                ## Google business
            try:
                google = driver.find_element("css selector", ".linkedin").get_attribute("href") 
            except:
                google = "No disponible"

                ## Instagram
            try:
                instagram = driver.find_element("css selector", ".instagram").get_attribute("href") 
            except:
                instagram = "No disponible"
            
            # Da click en siguente
            #driver.find_element("css selector", ".tit-nav-next").click()
            
            # ordenar tupla y añadirla a la lista
            lista_productor = (datos, imagen, descripcion, facebook, twitter, google, instagram)
            lista_datos.append(lista_productor)
        
            i += 1
            driver.back()     

        except:
            break

    # Cierra el navegador
    driver.close()

    return lista_datos

#%%

# Limpieza #
############

def limpiar_idiazabal(lista_datos):
    """
    Esta función toma una lista de listas con los productores de queso idiazabal (datos, imagen, descripcion, facebook, twitter, google, instagram), añade información como la dirección, ccaa, productos, y sello de calidad, lo ordena y lo guarda como un csv.
    
    
    Args:
    - lista_datos (list): lista de listas con los productores de queso idiazabal (datos, imagen, descripcion, facebook, twitter, google, instagram).

    Returns:
    - dataframe (DataFrame): Devuelve el dataframe de todos los datos recolectados y ordenados.
    - Guarda el dataframe en un archivo csv 'idiazabal.csv'
    """
    # Limpiar la string con la mayoría de datos (nombre, categoría,localidad - provincia, telefono, mail, web )
    datos_idiazabal = []
    for lista in lista_datos:
        lista_datos_productor = lista[0].split('\n')
        lista_datos_productor.extend(lista[1:])
        datos_idiazabal.append(lista_datos_productor)

    # Limpiar el resto de datos, separar localidad y provincia y añadir 'no disponible' en los datos faltantes
    telefono = 0
    mail = 0
    web = 0

    datos_limpios = []
    for lista_prod in datos_idiazabal:
        nombre = lista_prod[0]
        categoria = 'Lácteos'
        localidad = lista_prod[2].split("(")[0].strip()
        provincia = lista_prod[2].split("(")[1].replace(")", "")

        for elemento in lista_prod[:-6]:
            if elemento.replace(" ", "").replace("/", "").isnumeric():
                telefono = elemento
            if '@' in elemento:
                mail = elemento
            if 'http' in elemento:
                    web = elemento

        if not telefono:
            telefono = 'No disponible'
        if not mail:
            mail = 'No disponible'
        if not web:
            web = 'No disponible'

        lista_limpia = [nombre, categoria, localidad, provincia, telefono, mail, web]
        lista_limpia.extend(lista_prod[-6:])

    # Añadir información extra y oredenar para inserción en bbdd 

        # dirección
        lista_limpia.insert(2, "No disponible")

        # ccaa
        if lista_limpia[4] == 'Nafarroa/Navarra':
            lista_limpia.insert(5, "Navarra")
        else:    
            lista_limpia.insert(5, "País Vasco")
        
        # productos
        lista_limpia.insert(9, "Quesos")

        # sello de calidad
        lista_limpia.insert(10, "IGP Idiazabal")

        # cambios descripción
        try:
            print(lista_limpia[12])
            if lista_limpia[12]=='':
                lista_limpia[12] = 'No disponible'
            else:  
                lista_limpia[12] = lista_limpia[12].replace('Pulsar para la COMPRA DE QUESO', '').replace('Pulsar para la COMPRA DEL QUESO', '')
                print(f"modificat:\n{lista_limpia[12]}") 
        except:
            lista_limpia[12] = 'No disponible'
        
        datos_limpios.append(lista_limpia)

    # Lista de listas a dataframe
    dataframe = pd.DataFrame(datos_limpios)

    # Dataframe a csv
    dataframe.to_csv('idiazabal.csv', header=['nombre', 'categoria', 'direccion', 'localidad', 'provincia', 'ccaa', 'telefono', 'mail', 'web', 'productos', 'sello_de_calidad', 'url_imagen', 'descripcion', 'facebook', 'twitter', 'google', 'instagram'])

    return dataframe
# %%
