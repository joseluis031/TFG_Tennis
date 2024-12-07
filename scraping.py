import requests
from bs4 import BeautifulSoup

# URL del ranking ATP
url = "https://tennisabstract.com/reports/atpRankings.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extraer las filas de la tabla (excepto el encabezado)
tabla = soup.find("table")
filas = tabla.find_all("tr")[1:21]  # Top 20 (saltando el encabezado)

# Crear una lista para guardar las URLs de los jugadores
players = []
for fila in filas:
    columnas = fila.find_all("td")
    if len(columnas) >= 3:
        nombre = columnas[1].text.strip()  # Nombre del jugador
        url_jugador = columnas[1].find("a")["href"]  # Enlace al jugador
        full_url = f"https://tennisabstract.com/{url_jugador}"  # URL completa
        
        players.append({
            "Nombre": nombre,
            "URL": full_url
        })

# Mostrar los jugadores y sus URLs
for player in players:
    print(player)
