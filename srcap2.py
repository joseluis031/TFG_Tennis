from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configuración de Chrome sin interfaz gráfica
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Reemplaza con la ruta real de tu chromedriver si es necesario
driver = webdriver.Chrome(options=options)

# Cargar página
url = 'https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p=JannikSinner&f=ACareerqq'
driver.get(url)
time.sleep(3)  # Esperar a que se cargue el contenido dinámico

# Obtener HTML renderizado
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

# Extraer la tabla de partidos
table = soup.find('table', {'id': 'matches'})
rows = table.find_all('tr')

# Encabezados
headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]

# Datos
data = []
for row in rows[1:]:
    cols = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
    if cols:
        data.append(cols)

df = pd.DataFrame(data, columns=headers)
print(df.head())

# Guardar si quieres
df.to_csv("sinner_matches.csv", index=False)
