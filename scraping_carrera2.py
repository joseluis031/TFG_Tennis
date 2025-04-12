from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# Lista de jugadores
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
output_folder = "splits_results_last_52Weeks"
os.makedirs(output_folder, exist_ok=True)

# Configuración de Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

for player in players:
    print(f"Procesando splits de {player}...")
    driver = webdriver.Chrome(options=options)
    try:
        url = f"https://www.tennisabstract.com/cgi-bin/player.cgi?p={player}#splits"
        driver.get(url)

        # Esperar la tabla que contenga 'Split'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table//th[contains(text(), 'Split')]"))
        )

        soup = BeautifulSoup(driver.page_source, "lxml")
        tables = soup.find_all('table')

        matching_tables = []
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if 'Split' in headers and 'M' in headers and 'W' in headers:
                matching_tables.append(table)

        if len(matching_tables) >= 2:
            target_table = matching_tables[1]  # Segunda tabla que cumple la condición
            rows = target_table.find_all('tr')
            data = []
            for row in rows:
                cols = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                if cols:
                    data.append(cols)

            headers = data[0]
            data_rows = data[1:]
            df = pd.DataFrame(data_rows, columns=headers)

            output_path = os.path.join(output_folder, f"{player}_splits_last_52Weeks.csv")
            df.to_csv(output_path, index=False)
            print(f"Guardado en: {output_path}")
        else:
            print("No se encontró la segunda tabla de splits para", player)

    except Exception as e:
        print(f"Error con {player}: {e}")

    finally:
        driver.quit()
