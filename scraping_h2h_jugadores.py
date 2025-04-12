from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Lista de jugadores (como aparecen en la URL, con nombres sin espacios)
players = [
    'JannikSinner',
    'CarlosAlcaraz',
    'NovakDjokovic',
    'DaniilMedvedev',
    'AlexanderZverev',
    'StefanosTsitsipas',
    'AndreyRublev',
    'CasperRuud',
    'HubertHurkacz',
    'HolgerRune'
]

# Carpeta donde guardar resultados
output_folder = "h2h_results"
os.makedirs(output_folder, exist_ok=True)

# Configuración de Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

for player in players:
    print(f"\nProcesando H2H de {player}...")
    driver = webdriver.Chrome(options=options)
    try:
        url = f"https://www.tennisabstract.com/cgi-bin/player.cgi?p={player}#head-to-heads-h"
        driver.get(url)

        # Esperar a que aparezca la tabla con "Opponent"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table//th[contains(text(), 'Opponent')]"))
        )
        print("Tabla con 'Opponent' encontrada")

        soup = BeautifulSoup(driver.page_source, "lxml")
        tables = soup.find_all('table')

        h2h_table = None
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if 'Opponent' in headers and 'W' in headers and 'L' in headers:
                h2h_table = table
                break

        if h2h_table:
            print("Tabla H2H localizada. Extrayendo datos...")

            rows = h2h_table.find_all('tr')
            data = []
            for row in rows:
                cols = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                if cols:
                    data.append(cols)

            headers = data[0]
            data_rows = data[1:]
            df = pd.DataFrame(data_rows, columns=headers)

            output_path = os.path.join(output_folder, f"{player}_h2h.csv")
            df.to_csv(output_path, index=False)
            print(f"Guardado en: {output_path}")
        else:
            print("No se encontró la tabla H2H con columnas esperadas.")

    except Exception as e:
        print(f"Error con {player}: {e}")

    finally:
        driver.quit()
