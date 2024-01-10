
# Proyecto Base de Datos de Productores Locales

Este proyecto tiene como objetivo la creación de una base de datos de productores locales. Actualemente, unicamente incluye la extracción de datos de los productores de queso Idiazabal y txakolí de Álava. Para ello, se ha desarrollado un script en Python que realiza la extracción de datos desde el sitio web [quesoidiazabal.com](https://www.quesoidiazabal.eus/productores) utilizando Selenium y la extracción de datos de [txakolidealava.eus](https://txakolidealava.eus/bodegas/) mediante Selenium y Beautiful Soup.

## Contenido del Repositorio

- **`src`**: Carpeta contenedora de los scripts de python
    - **`idiazabal.py`**: Contiene el código principal para la extracción de datos de la web de quesos idiazabal

- **`data`**: Carpeta contenedora de los diferentes datos en formato csv.

- **`main.py`**: Este archivo contiene el script principal para la extracción y limpieza de datos desde la web de quesos Idiazabal.
- **`README.md`**: Este archivo que proporciona información sobre el proyecto.

## Requisitos del Sistema

Para ejecutar el script, se requiere tener instalado Python y las siguientes librerías:

```bash
pip install pandas selenium
```

Este proyecto realiza la extracción con el navegador web Firefox (modifiquesé el navegador a utilizar si fuera necesario:  
`driver = webdriver.Firefox()`)

## Librerías Utilizadas

El proyecto utiliza las siguientes librerías de Python:

- **Pandas**: Librería poderosa para manipulación y análisis de datos. [Documentación](https://pandas.pydata.org/pandas-docs/stable/)

- **Selenium**: Framework para la automatización de navegadores web. Utilizado en este proyecto para extraer datos de la web. [Documentación](https://www.selenium.dev/documentation/en/)

- **Time (sleep)**: Librería estándar de Python utilizada para pausar la ejecución del script. [Documentación](https://docs.python.org/3/library/time.html)

## Estructura de Datos

El archivo CSV resultante de la extracción y limpieza de los datos tiene las siguientes columnas:

- `nombre`: Nombre.
- `categoria`: Categoría de los productods producidos:Lácteors, Carnes, Huevos, Bebidas, Bebidas alcoholicas, Verduras, Frutas).
- `direccion`: Dirección.
- `localidad`: Localidad.
- `provincia`: Provincia.
- `ccaa`: Comunidad Autónoma (CCAA).
- `telefono`: Número de teléfono de contacto.
- `mail`: Correo electrónico de contacto.
- `web`: Sitio web.
- `productos`: Tipo de productos ofrecidos.
- `sello_de_calidad`: Sello de calidad asociado.
- `url_imagen`: URL de la imagen.
- `descripcion`: Descripción de la producción.
- `facebook`: Enlace al perfil de Facebook.
- `twitter`: Enlace al perfil de Twitter.
- `google`: Enlace a la página de Google Business.
- `instagram`: Enlace al perfil de Instagram.

## Licencia

Este proyecto está bajo la licencia Creative Commons Attribution 4.0 International License.

![cc-by-image](https://i.creativecommons.org/l/by/4.0/88x31.png)


