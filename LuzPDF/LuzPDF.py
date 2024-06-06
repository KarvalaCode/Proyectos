#%%
# Importaciones #
#################

# Importar fitz para usar pymupdf (fitz es pymupdf)
# -----------------------------------------------------------------------
import fitz

# Importar la biblioteca pendulum y datetime para trabajar con fechas
# -----------------------------------------------------------------------
from datetime import datetime
import pendulum

# Importar regex
# -----------------------------------------------------------------------
import re

# Importar la biblioteca pgcode para trabajar con codigos postales
# -----------------------------------------------------------------------
import pgeocode

# Importar la biblioteca json para trabajar con este tipo de archivos
# -----------------------------------------------------------------------
import json

# Configuración bibliotecas #
#############################

# Definir timezone e idioma en la biblioteca pendulum
# -----------------------------------------------------------------------
tz = pendulum.timezone('Europe/Paris')
pendulum.set_locale('es')

# Funciones lectura y extracción de información de PDFs #
##########################################################

def formato_fecha(fecha):
    """ Comprueba si al fecha está en formato: "DD.MM.YYYY" y si no, convierte las fechas en formato DD/MM/YYYY o "DD de MMMM YYYY" al formato DD.MM.YYYY.
    Args:
        fecha (Date or String): fecha a comprobar/cambiar de formato.
    Returns:
        dt_final (Date): devuelve la fecha con el formato cambiado.
    """

    dt = ''

    # Comprobar si la fecha está en formato adecuado y si no convertirla.
    try:
        datetime.strptime(fecha, "%d.%m.%Y")
        return fecha
    except ValueError:
        if '/' in fecha:
            dt = pendulum.from_format(fecha, 'DD/MM/YYYY')
        elif 'de' in fecha:
            dt = pendulum.from_format(fecha.replace(' de', ''), 'DD MMMM YYYY')
        else:
            dt_final = fecha
        try:
            dt_final = dt.format('DD.MM.YYYY')
        except Exception:
            dt_final = fecha

        return dt_final  
    
def separa_CP(direccion):
    """ Divide una string en una lista por un código de 5 dígitos (incluido en la lista devuelta).
    Args:
        direccion (String): línea de texto que incluya un código postal.
    Returns:
        lista (list): devuelve una lista separando por el código postal. 
    """
    return re.split(r"(\d{5})", direccion)

def extaer_pag_pdf(ruta, num):
    """ Extrae el texto de un pdf en formato string convirtiéndolo en una lista dónde cada línea del texto es un elemento (string) de la lista.
    Args:
        ruta (String): ruta al archivo pdf que se va a leer.
        num (int): número de la página del pdf que se quiere leer (empezando en 0).
    Returns:
        lista (list): devuelve una lista separando cada línea del texto como un elemento de la lista.
    """
    file = fitz.open(ruta)
    pymupdf_text = []

    for page in file:
        pymupdf_text.append(page.get_text())

    return pymupdf_text[num].split('\n')  

def pdf_a_dicc_y_lista(lineas_pdf):
    """ De una lista de strings, se eliminan las líneas vacias y se crea un diccionario con los elementos de los que se pueden extraer pares key/valor mediante la separación por ':' y, por otro lado, se crea una lista con todos los elementos para tenerlos ordenados.
    Args:
        lineas_pdf (list): lista de strings.
    Returns:
        dict_lineas(dict): devuelve un diccionario con los pares key/valor de las líneas que incluyan ':' y el resto de líneas con una key numerada.
        lista_lineas (list): devuelve una lista donde cada elemnto es una string (misma lista de args sin elementos vacíos).
    """
    dict_lineas = {}
    lista_lineas = []
    contador = 0
    for linea in lineas_pdf:
        linea = linea.strip()
        # Se eliminan lineas vacias
        if linea != '':
            lista_lineas.append(linea)
            # Se dividen las líneas por el primer ':' para separarlas en Key/valor en el diccionario
            if ':' in linea:
                lista_linea = linea.split(':', 1)
                dict_lineas[lista_linea[0]] = lista_linea[1].strip() 
            else:
                # En caso de no contar con ':' en la línea, se añade al diccionario con la key:'otro' más un número incremental
                contador += 1
                dict_lineas[f'otro{contador}'] = linea
    return dict_lineas, lista_lineas

def extraer_info(dict_lineas, lista_lineas):
    """ A partir de un diccionario y una lista de strings, se extrae toda la información necesaria en otro diccionario
    Args:
        dict_lineas (dict): diccionario de strings proveniente de la lectura de un pdf.
        lista_lineas (list): lista de strings proveniente de la lectura del mismo pdf.
    Returns:
        diccionario_final (dict): devuelve un diccionario con los datos extaridos del diccioanrio y la lista de la lectura del pdf.
    """

    # Crear el diccionario que se convertirá en el archivo JSON final con los datos a conseguir
    diccionario_final = {
    "nombre_cliente": "",
    "dni_cliente": "",
    "calle_cliente": "",
    "cp_cliente": "",
    "población_cliente": "",
    "provincia_cliente": "",
    "nombre_comercializadora": "",
    "cif_comercializadora": "",
    "dirección_comercializadora": "",
    "cp_comercializadora": "",
    "población_comercializadora": "",
    "provincia_comercializadora": "",
    "número_factura": "",
    "inicio_periodo": "",
    "fin_periodo": "",
    "importe_factura": "",
    "fecha_cargo": "",
    "consumo_periodo": "",
    "potencia_contratada": ""
    }

    # Se obtienen todos los datos que se pueden extraer mediante las llaves del diccionario 
    for key in dict_lineas.keys():
        try:
            if 'nº' in key.lower() and 'factura' in key.lower():
                diccionario_final["número_factura"] = dict_lineas[key].split()[0]
            if 'periodo' in key.lower() or 'período' in key.lower():
                lista_fechas = dict_lineas[key].replace('del', '').replace('de', '').split('(')[0]
                if 'al' in dict_lineas[key].lower():
                    fechas_consumo = lista_fechas.split(' al ')
                elif 'a' in dict_lineas[key].lower():    
                    fechas_consumo = lista_fechas.split(' a ')
                diccionario_final["inicio_periodo"] = formato_fecha(fechas_consumo[0].strip())
                diccionario_final["fin_periodo"] = formato_fecha(fechas_consumo[-1].strip())
            
            if 'potencia' in key.lower() and 'importe' not in key.lower():
                try:
                    diccionario_final["potencia_contratada"] = str(float(dict_lineas[key].split()[0].replace(',','.'))).replace('.',',')
                except Exception:
                    continue

            if 'titular' in key.lower() or 'nombre' in key.lower() :
                diccionario_final["nombre_cliente"] = dict_lineas[key]     
            if 'dirección' in key.lower():
                try:
                    lista_direccion = separa_CP(dict_lineas[key])
                    diccionario_final["calle_cliente"] = lista_direccion[0]
                    diccionario_final["cp_cliente"] = lista_direccion[1]
                    diccionario_final["población_cliente"] = lista_direccion[2]
                    if diccionario_final["calle_cliente"] != '' and diccionario_final["cp_cliente"] != '' and diccionario_final["población_cliente"] != '':
                        break
                    else:
                        continue 
                except Exception:
                    continue
        except Exception:
            continue
    # Se duplica el for en el caso para poder romper el loop después de la primera localización y asegurarnos que es el dato correcto (ya que estos suelen estasr al principio de la factura).
    for key in dict_lineas.keys():
        if 'domicilio' in key.lower() and 'social' in key.lower():
            direccion_comercializadora = separa_CP(dict_lineas[key])
            try:
                if len(direccion_comercializadora[1]) == 5: 
                    diccionario_final["dirección_comercializadora"] = direccion_comercializadora[0].strip()
                    diccionario_final["cp_comercializadora"] = direccion_comercializadora[1].strip() 
            except Exception:
                continue 

    for key in dict_lineas.keys():
        if 'fecha' in key.lower() and 'cargo' in key.lower():
            diccionario_final["fecha_cargo"] = formato_fecha(dict_lineas[key])
            break
    for key in dict_lineas.keys():
        if 'diccionario_final["fecha_cargo"]' == '' and 'fecha' in key.lower() and 'emisión' in key.lower():
                diccionario_final["fecha_cargo"] = formato_fecha(dict_lineas[key])
                break
            
    for key in dict_lineas.keys():
        try:
            if 'importe' in key.lower() and 'factura' in key.lower():
                diccionario_final["importe_factura"] = dict_lineas[key].split()[0]
                break
        except Exception:
            continue    

    for key in dict_lineas.keys():
        if 'nif' in key.lower():
            diccionario_final["dni_cliente"] = dict_lineas[key]  
            break

    # Mediante un enumerate extraemos todos los datos que sabemos que estan cerca unos de otros en la lista.
    lista_direccion = []
    for indice, linea in enumerate(lista_lineas):
        if 'potencia' in linea.lower() and diccionario_final["potencia_contratada"] == '':
            if 'kw' in lista_lineas[indice+1].lower():
                try: 
                    diccionario_final["potencia_contratada"] = str(float(lista_lineas[indice+1].split()[0].replace(',','.'))).replace('.', ',') 
                except Exception:
                    continue
        if diccionario_final["dni_cliente"] == '' or diccionario_final["dni_cliente"] == None or len(diccionario_final["dni_cliente"]) != 9:
            try:
                dni = re.search(r"[0-9]{8}[A-Za-z]", linea)
                diccionario_final["dni_cliente"] = dni.group()
            except Exception:
                continue
        
        if (diccionario_final["inicio_periodo"] == '' or diccionario_final["fin_periodo"] == '') and ('periodo' in linea.lower() or 'período' in linea.lower()):
            fechas = linea.replace('periodo', '').replace('período', '').replace('Periodo', '').replace('Período', '').replace('del', '').replace('de', '').strip()
            
            if 'a' in linea.lower():    
                fechas_consumo = fechas.split(' a ')
            elif 'al' in linea.lower():
                fechas_consumo = fechas.split(' al ')
    
            diccionario_final["inicio_periodo"] = formato_fecha(fechas_consumo[0].strip())
            diccionario_final["fin_periodo"] = formato_fecha(fechas_consumo[-1].strip())
                
        if 'dirección' in linea.lower() and 'suministro' in linea.lower() and diccionario_final["calle_cliente"] == '':
            try:
                lista_direccion.append(linea) 
                lista_direccion.append(lista_lineas[indice+1]) 
                direccion_suministro = ' '.join(lista_direccion)
                direccion_dividir = direccion_suministro.split(':', 1)
                direccion = direccion_dividir[1].strip().split(',')
                diccionario_final["calle_cliente"] = direccion[0].strip() 
                diccionario_final["población_cliente"] = direccion[1].strip()  
            except Exception:
                direccion_entera = linea.split(':', 1)[1]
                direccion = separa_CP(direccion_entera)
                diccionario_final["calle_cliente"] = direccion[0].strip() 
                diccionario_final["población_cliente"] = direccion[2].strip()  
        
        
    # Se duplican los bucles for para poder pararlos después de la primera aparición en aquella información repetida a lo largo del pdf y que puede dar problemas.
    for indice, linea in enumerate(lista_lineas):
        if ('importe' in linea.lower() and 'factura' in linea.lower()) or ('total' in linea.lower() and 'pagar' in linea.lower()) and (diccionario_final["importe_factura"] == '' or diccionario_final["importe_factura"] <= 0.0):
            try:
                importe = float(lista_lineas[indice-1].split()[0].replace(',','.'))
                diccionario_final["importe_factura"] = str(importe).replace('.',',')               
            except Exception:
                lista_importe = lista_lineas[indice].replace(',','.').split()
                for elemento in lista_importe:
                    try:
                        importe = float(elemento)
                        diccionario_final["importe_factura"] = str(importe).replace('.', ',')
                        break
                    except Exception:
                        continue
                
    for indice, linea in enumerate(lista_lineas):
        if 'cif' in linea.lower():
            diccionario_final["cif_comercializadora"] = linea.split()[-1].replace('.', '').strip()
            try:
                if len(diccionario_final["cif_comercializadora"]) != 9:
                    diccionario_final["cif_comercializadora"] = ''
                    diccionario_final["cif_comercializadora"] = lista_lineas[indice+1].replace('.', '').strip()
                break
            except Exception:
                continue
    for indice, linea in enumerate(lista_lineas):
        if 'cif' in linea.lower():
            try:                
                diccionario_final["nombre_comercializadora"] = lista_lineas[indice-1]
                nombre = re.search(r"^[\sáéíóúÁÉÍÓÚàÀÈÈÒòa-z,A-Z]+S\.[AL]\.", diccionario_final["nombre_comercializadora"])
                diccionario_final["nombre_comercializadora"] = nombre.group()
            except Exception:
                continue
            for x in range(-2, 3):
                direccion_comercializadora = separa_CP(lista_lineas[indice+x])
                try:
                    if len(direccion_comercializadora[1]) == 5: 
                        diccionario_final["dirección_comercializadora"] = direccion_comercializadora[0].strip()
                        diccionario_final["cp_comercializadora"] = direccion_comercializadora[1].strip()
                        break      
                    else:
                        continue    
                except IndexError:
                    continue     
            
    for indice, linea in enumerate(lista_lineas):
        if (diccionario_final["dirección_comercializadora"] == '' or len(diccionario_final["dirección_comercializadora"]) < 5) and 'social' in linea.lower():
            try:
                lista_comercializadora = linea.split(':', 1)
                nombre = re.search(r"^[\sa-z,A-Z]+S\.[AL]\.", lista_comercializadora[0])
                diccionario_final["nombre_comercializadora"] = nombre.group()

                lista_direccion_comercial = separa_CP(lista_comercializadora[-1])
                if len(lista_direccion_comercial[1]) == 5: 
                    diccionario_final["dirección_comercializadora"] = lista_direccion_comercial[0].strip()
                    diccionario_final["cp_comercializadora"] = lista_direccion_comercial[1]
                    break
            except:
                continue

    for indice, linea in enumerate(lista_lineas):
        if 'cif' in linea.lower():        
            try:
                if diccionario_final["nombre_cliente"] == '':
                    diccionario_final["nombre_cliente"] = lista_lineas[indice+2]
                    if diccionario_final["calle_cliente"] == '':
                        diccionario_final["calle_cliente"] = lista_lineas[indice+3]
                    break
            except Exception:
                continue        
                     
    for indice, linea in enumerate(lista_lineas):
        if 'consumo' in linea.lower() and 'p1' in linea.lower() and diccionario_final["consumo_periodo"] == '':
            try: 
                consumo = int(lista_lineas[indice+1].split('kWh')[0].strip())
                diccionario_final["consumo_periodo"] = consumo
                break 
            except Exception:
                continue

    for indice, linea in enumerate(lista_lineas):
        if 'consumo' in linea and (diccionario_final['consumo_periodo'] == '' or 'xx' in str(diccionario_final['consumo_periodo']).lower()):
            for x in range(1,5):
                if 'kwh' in lista_lineas[indice+x].lower():
                    try:
                        diccionario_final['consumo_periodo'] = int(linea.split()[0])
                        if diccionario_final['consumo_periodo'] != '' or 'xx' not in str(diccionario_final['consumo_periodo']).lower():
                            break
                    except Exception:
                        continue

    for indice, linea in enumerate(lista_lineas):
        if diccionario_final['cp_cliente'] == '':
            if diccionario_final['nombre_cliente'].lower() in linea.lower():
                try:
                    cp = re.search(r"[\d]{5}", lista_lineas[indice+2])
                    diccionario_final["cp_cliente"] = cp.group()
                    diccionario_final["calle_cliente"] = lista_lineas[indice+1]
                    break
                except AttributeError:
                    continue

                           
    nomi = pgeocode.Nominatim('es')
    diccionario_final["provincia_cliente"] = nomi.query_postal_code(diccionario_final["cp_cliente"])['county_name']              
    diccionario_final["población_cliente"] = nomi.query_postal_code(diccionario_final["cp_cliente"])['place_name']              
    diccionario_final["provincia_comercializadora"] = nomi.query_postal_code(diccionario_final["cp_comercializadora"])['county_name']       
    diccionario_final["población_comercializadora"] = nomi.query_postal_code(diccionario_final["cp_comercializadora"])['place_name']       

    for linea in lista_lineas:
        lista_pueblos = str(diccionario_final["población_cliente"]).split(',')
        for pueblo in lista_pueblos:
            pueblo = pueblo.strip()
            if pueblo.lower() in linea.lower():
                diccionario_final["población_cliente"] = pueblo
                break
    for linea in lista_lineas:
        lista_pueblos = str(diccionario_final["población_comercializadora"]).split(',')
        for pueblo in lista_pueblos:
            pueblo = pueblo.strip()
            if pueblo.lower() in linea.lower():
                diccionario_final["población_comercializadora"] = pueblo
                break
    print(lista_lineas)            
    return diccionario_final



def lectura_y_extraccion(ruta, min, max, pag=0):
    """ A partir de una carpeta con PDFs con formato "factura_x.pdf", extrae la informaciónd de la primera página en un diccionario, en caso de que algun campo del diccionario final quede vacío, se busca esa información en la segunda página del pdf
    Args:
        ruta (String): ruta hacia la capeta que contiene lso PDFs
        min (int): número de factura más pequeño
        max (int): número de factura más grande
        pag (int): Número de página del pdf que se quiere leer (empezando en 0). Por defecto es la primera(0).
    Returns:
        diccionario_final (dict): devuelve el diccionario final que se habrà convetido en json.
    """
    for num_pdf in range (min, max+1):
        num_pdf = str(num_pdf)
        ruta_pdf = f"{ruta}/factura_{num_pdf}.pdf"
        lineas_pdf = extaer_pag_pdf(ruta_pdf, pag)
        dict_lineas, lista_lineas = pdf_a_dicc_y_lista(lineas_pdf)
        diccionario_final = extraer_info(dict_lineas, lista_lineas)
        for key in diccionario_final.keys():
            if diccionario_final[key] == '':
                lineas_pdf2 = extaer_pag_pdf(ruta_pdf, pag+1)
                dict_lineas2, lista_lineas2 = pdf_a_dicc_y_lista(lineas_pdf2)
                diccionario_final2 = extraer_info(dict_lineas2, lista_lineas2)
                diccionario_final[key] = diccionario_final2[key]
            
        with open(f"json_final/factura_{str(num_pdf)}_final.json", "w") as fp:
            json.dump(diccionario_final, fp, ensure_ascii=False)
    return diccionario_final            