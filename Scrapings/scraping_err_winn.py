from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import os

# Diccionario de jugadores con su ID en TennisAbstract
players = {
    'CarlosAlcaraz': '207989/Carlos-Alcaraz',
    'JannikSinner': '206173/Jannik-Sinner',
    'NovakDjokovic': '104925/Novak-Djokovic',
    'DaniilMedvedev': '106421/Daniil-Medvedev',
    'AlexanderZverev': '100644/Alexander-Zverev',
    'StefanosTsitsipas': '126774/Stefanos-Tsitsipas',
    'AndreyRublev': '126094/Andrey-Rublev',
    'CasperRuud': '134770/Casper-Ruud',
    'HubertHurkacz': '128034/Hubert-Hurkacz',
    'HolgerRune': '208029/Holger-Rune'
}

# Carpeta de salida
output_folder = "winners_errors_results"
os.makedirs(output_folder, exist_ok=True)

# Configurar Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

for name, player_path in players.items():
    print(f"Procesando tabla de winners/errors para {name}...")
    url = f"https://www.tennisabstract.com/cgi-bin/player-more.cgi?p={player_path}&table=winners-errors"

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )

        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')

        if len(tables) > 8:
            table = tables[8]
            rows = table.find_all('tr')
            data = []
            for row in rows:
                cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                if cols:
                    data.append(cols)

            headers = data[0]
            data_rows = data[1:]
            df = pd.DataFrame(data_rows, columns=headers)

            output_path = os.path.join(output_folder, f"{name}_winners_errors.csv")
            df.to_csv(output_path, index=False)
            print(f"Guardado en: {output_path}")
        else:
            print(f"No se encontró la tabla 8 para {name}")

    except TimeoutException:
        print(f"Tiempo de espera agotado para {name}")

    except Exception as e:
        print(f"Error inesperado con {name}: {e}")

    finally:
        driver.quit()
