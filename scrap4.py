from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import os

# Diccionario con nombres e IDs de jugadores
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

# Configuración Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

def scrape_table(player_name, player_path, table_name, output_subfolder, suffix):
    url = f"https://www.tennisabstract.com/cgi-bin/player-more.cgi?p={player_path}&table={table_name}"
    output_folder = os.path.join(output_subfolder)
    os.makedirs(output_folder, exist_ok=True)

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//table")))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tables = soup.find_all('table')

        # Buscar tabla más consistente (mayor número de columnas en la primera fila)
        best_table = None
        max_cols = 0
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue
            headers = [col.get_text(strip=True) for col in rows[0].find_all(['td', 'th'])]
            if len(headers) > max_cols:
                max_cols = len(headers)
                best_table = table

        if best_table:
            data = []
            for row in best_table.find_all('tr'):
                cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                if cols:
                    data.append(cols)

            headers = data[0]
            data_rows = [row for row in data[1:] if len(row) == len(headers)]
            df = pd.DataFrame(data_rows, columns=headers)

            output_path = os.path.join(output_folder, f"{player_name}_{suffix}.csv")
            df.to_csv(output_path, index=False)
            print(f"{suffix} guardado para {player_name} en: {output_path}")
        else:
            print(f"No se encontró una tabla válida para {player_name} ({suffix})")

    except TimeoutException:
        print(f"Tiempo de espera agotado para {player_name} ({suffix})")
    except Exception as e:
        print(f"Error con {player_name} ({suffix}): {e}")
    finally:
        driver.quit()

def scrape_mcp_serve():
    for name, path in players.items():
        scrape_table(name, path, "mcp-serve", "calidad_servicio", "servicio")

def scrape_mcp_return():
    for name, path in players.items():
        scrape_table(name, path, "mcp-return", "calidad_resto", "resto")

def scrape_mcp_rally():
    for name, path in players.items():
        scrape_table(name, path, "mcp-rally", "calidad_rally", "rally")

def scrape_mcp_tactics():
    for name, path in players.items():
        scrape_table(name, path, "mcp-tactics", "calidad_tactics", "tactics")

def main():
    #scrape_mcp_serve()
    #scrape_mcp_return()
    scrape_mcp_rally()
    scrape_mcp_tactics()

if __name__ == "__main__":
    main()
