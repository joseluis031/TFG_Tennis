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

            output_path = os.path.join(output_folder, f"{player_name}_{suffix}.csv")
            df.to_csv(output_path, index=False)
            print(f"{suffix} guardado para {player_name} en: {output_path}")
        else:
            print(f"No se encontró la tabla 8 para {player_name} ({suffix})")

    except TimeoutException:
        print(f"Tiempo de espera agotado para {player_name} ({suffix})")
    except Exception as e:
        print(f"Error con {player_name} ({suffix}): {e}")
    finally:
        driver.quit()

def scrape_winners_errors():
    for name, path in players.items():
        scrape_table(name, path, "winners-errors", "winners_errors_results2", "winners_errors")

def scrape_key_points():
    for name, path in players.items():
        scrape_table(name, path, "pbp-points", "key_points_results2", "key_points")

def scrape_key_games():
    for name, path in players.items():
        scrape_table(name, path, "pbp-games", "key_games_results2", "key_games")

def scrape_point_by_point_stats():
    for name, path in players.items():
        scrape_table(name, path, "pbp-stats", "point_by_point_stats_results2", "pbp_stats")

def main():
    scrape_winners_errors()
    scrape_key_points()
    scrape_key_games()
    scrape_point_by_point_stats()

if __name__ == "__main__":
    main()
