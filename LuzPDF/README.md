
# Proyecto de Extracción de Información de Facturas en PDF

Este proyecto tiene como objetivo leer y extraer información relevante de archivos PDF de facturas y guardarla en archivos JSON. Utiliza varias bibliotecas de Python para el manejo de fechas, textos, expresiones regulares y archivos PDF.

## Requisitos

- Python 3.7 o superior
- Bibliotecas Python:
  - [`pymupdf (fitz)`](https://pymupdf.readthedocs.io/en/latest/): Biblioteca para manipular documentos PDF.
  - [`pendulum`](https://pendulum.eustace.io/): Biblioteca para manejar y manipular fechas y horas.
  - [`pgeocode`](https://pgeocode.readthedocs.io/en/latest/): Biblioteca para manipular y obtener información sobre códigos postales.
  - [`json`](https://docs.python.org/3/library/json.html): Módulo para trabajar con datos en formato JSON.
  - [`re`](https://docs.python.org/3/library/re.html): Módulo para trabajar con expresiones regulares.
  - [`datetime`](https://docs.python.org/3/library/datetime.html): Módulo para trabajar con fechas y horas.

Puedes instalar las bibliotecas necesarias usando el siguiente comando:

```bash
pip install pymupdf pendulum pgeocode
```

## Estructura del Proyecto

- `LuzPDF.py`: Contiene las funciones principales para leer y extraer información de los archivos PDF.
- `main.py`: Script principal que importa las funciones de `LuzPDF.py` y ejecuta la extracción de información.
- Carpeta `pdfs`: Contiene los archivos PDF a procesar.
- Carpeta `json_final`: Contiene los archivos JSON generados.

## Uso

### Ejecución del Script Principal

El script `main.py` lee todos los archivos PDF en la carpeta `pdfs` y extrae la información relevante, guardándola en archivos JSON en la carpeta `json_final`.

Para ejecutar el script, simplemente ejecuta el siguiente comando en tu terminal:

```bash
python main.py
```

### Funciones Principales

#### `formato_fecha(fecha)`

Convierte fechas en varios formatos al formato `DD.MM.YYYY`.

#### `separa_CP(direccion)`

Divide una cadena en una lista por un código postal de 5 dígitos.

#### `extaer_pag_pdf(ruta, num)`

Extrae el texto de una página específica de un archivo PDF y lo devuelve como una lista de líneas.

#### `pdf_a_dicc_y_lista(lineas_pdf)`

Convierte una lista de líneas de texto en un diccionario de pares clave/valor y una lista ordenada.

#### `extraer_info(dict_lineas, lista_lineas)`

Extrae información específica de un diccionario y una lista de líneas, y la organiza en un diccionario final.

#### `lectura_y_extraccion(ruta, min, max, pag=0)`

Lee múltiples archivos PDF en una carpeta y extrae la información de la primera página, buscando en la segunda página si falta alguna información.

## Estructura de Archivos JSON

Cada archivo JSON generado tendrá la siguiente estructura:

```json
{
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
```

## Licencia

Este proyecto está bajo la licencia Creative Commons Attribution 4.0 International License.

![cc-by-image](https://i.creativecommons.org/l/by/4.0/88x31.png)

---

```markdown
# PDF Invoice Information Extraction Project

This project aims to read and extract relevant information from PDF invoice files and save it into JSON files. It utilizes several Python libraries for handling dates, text, regular expressions, and PDF files.

## Requirements

- Python 3.7 or higher
- Python Libraries:
  - [`pymupdf (fitz)`](https://pymupdf.readthedocs.io/en/latest/): Library for manipulating PDF documents.
  - [`pendulum`](https://pendulum.eustace.io/): Library for handling and manipulating dates and times.
  - [`pgeocode`](https://pgeocode.readthedocs.io/en/latest/): Library for handling and retrieving information about postal codes.
  - [`json`](https://docs.python.org/3/library/json.html): Module for working with JSON data.
  - [`re`](https://docs.python.org/3/library/re.html): Module for working with regular expressions.
  - [`datetime`](https://docs.python.org/3/library/datetime.html): Module for working with dates and times.

You can install the required libraries using the following command:

```bash
pip install pymupdf pendulum pgeocode
```

## Project Structure

- `LuzPDF.py`: Contains the main functions for reading and extracting information from PDF files.
- `main.py`: Main script that imports functions from `LuzPDF.py` and executes the information extraction.
- `pdfs` folder: Contains the PDF files to be processed.
- `json_final` folder: Contains the generated JSON files.

## Usage

### Running the Main Script

The `main.py` script reads all PDF files in the `pdfs` folder and extracts relevant information, saving it into JSON files in the `json_final` folder.

To run the script, simply execute the following command in your terminal:

```bash
python main.py
```

### Main Functions

#### `formato_fecha(fecha)`

Converts dates in various formats to the `DD.MM.YYYY` format.

#### `separa_CP(direccion)`

Splits a string into a list by a 5-digit postal code.

#### `extaer_pag_pdf(ruta, num)`

Extracts text from a specific page of a PDF file and returns it as a list of lines.

#### `pdf_a_dicc_y_lista(lineas_pdf)`

Converts a list of text lines into a dictionary of key/value pairs and an ordered list.

#### `extraer_info(dict_lineas, lista_lineas)`

Extracts specific information from a dictionary and a list of lines, organizing it into a final dictionary.

#### `lectura_y_extraccion(ruta, min, max, pag=0)`

Reads multiple PDF files in a folder and extracts information from the first page, looking at the second page if any information is missing.

## JSON File Structure

Each generated JSON file will have the following structure:

```json
{
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
```

## License

This project is licensed under the Creative Commons Attribution 4.0 International License.

![cc-by-image](https://i.creativecommons.org/l/by/4.0/88x31.png)
```
