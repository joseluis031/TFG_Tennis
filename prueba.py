import requests
from bs4 import BeautifulSoup

# URL de la página con la tabla
url = "https://tennisabstract.com/cgi-bin/leaders.cgi"

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code != 200:
    raise Exception(f"Error al acceder a la página: {response.status_code}")

# Analizar el contenido de la página
soup = BeautifulSoup(response.text, "html.parser")

# Listar todas las tablas en el HTML
tablas = soup.find_all("table")

# Imprimir el número de tablas encontradas
print(f"Número de tablas encontradas: {len(tablas)}")

# Inspeccionar cada tabla
for idx, tabla in enumerate(tablas):
    print(f"\nTabla {idx}:")
    print(tabla.prettify()[:500])  # Mostrar los primeros 500 caracteres de cada tabla

# Seleccionar la tabla correcta (cambiar el índice según corresponda)
tabla_correcta = tablas[1]  # Ajusta este índice según la tabla que contiene los datos

# Extraer encabezados
encabezados = [th.text.strip() for th in tabla_correcta.find_all("th")]
print("\nEncabezados encontrados:", encabezados)

# Extraer las filas de la tabla
filas = tabla_correcta.find_all("tr")

# Procesar las filas para obtener los datos
tabla_datos = []
for fila in filas:
    celdas = fila.find_all("td")
    if celdas:  # Ignorar filas sin celdas
        fila_datos = [celda.text.strip() for celda in celdas]
        tabla_datos.append(fila_datos)

# Mostrar las primeras 20 filas de la tabla
print("\nPrimeras 20 filas de la tabla extraída:")
for fila in tabla_datos[:20]:
    print(fila)
