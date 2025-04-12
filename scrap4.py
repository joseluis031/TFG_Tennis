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

# Configuración Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

def scrape_mcp_table(table_name, output_folder, suffix):
    os.makedirs(output_folder, exist_ok=True)
    for name, player_path in players.items():
        print(f"Procesando {suffix} para {name}...")
        url = f"https://www.tennisabstract.com/cgi-bin/player-more.cgi?p={player_path}&table={table_name}"

        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//table")))
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

                output_path = os.path.join(output_folder, f"{name}_{suffix}.csv")
                df.to_csv(output_path, index=False)
                print(f"Guardado en: {output_path}")
            else:
                print(f"No se encontró la tabla 8 para {name} ({suffix})")

        except TimeoutException:
            print(f"Tiempo de espera agotado para {name} ({suffix})")
        except Exception as e:
            print(f"Error inesperado con {name} ({suffix}): {e}")
        finally:
            driver.quit()

def main():
    scrape_mcp_table("mcp-serve", "calidad_servicio", "servicio")
    scrape_mcp_table("mcp-return", "calidad_de_resto", "resto")
    scrape_mcp_table("mcp-rally", "calidad_rally", "rally")
    scrape_mcp_table("mcp-tactics", "calidad_tactics", "tactics")

if __name__ == "__main__":
    main()
