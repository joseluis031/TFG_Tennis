from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os

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

# Configuración headless
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Crear carpetas de salida
os.makedirs("splits_results2", exist_ok=True)
os.makedirs("splits_results_52weeks2", exist_ok=True)
os.makedirs("rankings_results2", exist_ok=True)
os.makedirs("h2h_results2", exist_ok=True)

def get_table_from_url(url, table_condition, table_index=None):
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        soup = BeautifulSoup(driver.page_source, "lxml")
        tables = soup.find_all("table")

        if table_index is not None and table_index < len(tables):
            return tables[table_index]
        else:
            for table in tables:
                headers = [th.get_text(strip=True) for th in table.find_all("th")]
                if table_condition(headers):
                    return table
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
    finally:
        driver.quit()
    return None

def get_second_matching_table(url, condition):
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        soup = BeautifulSoup(driver.page_source, "lxml")
        tables = soup.find_all("table")

        matching_tables = []
        for table in tables:
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            if condition(headers):
                matching_tables.append(table)

        if len(matching_tables) >= 2:
            return matching_tables[1]
    except Exception as e:
        print(f"Error al acceder a {url}: {e}")
    finally:
        driver.quit()
    return None


def table_to_csv(table, jugador, output_path):
    rows = table.find_all("tr")
    data = [[cell.get_text(strip=True) for cell in row.find_all(["td", "th"])] for row in rows if row.find_all(["td", "th"])]
    if data:
        headers, data_rows = data[0], data[1:]
        df = pd.DataFrame(data_rows, columns=headers)
        df.to_csv(output_path, index=False)
        print(f"Guardado en: {output_path}")

for player in players:
    print(f"\nProcesando a {player}...")

    # SPLITS carrera
    url_splits = f"https://www.tennisabstract.com/cgi-bin/player.cgi?p={player}#year-end-rankings-h"
    table = get_table_from_url(url_splits, lambda headers: 'Split' in headers and 'M' in headers)
    if table:
        output_file = f"splits_results2/{player}_splits2.csv"
        table_to_csv(table, player, output_file)

    # SPLITS 52 semanas
    url_52 = f"https://www.tennisabstract.com/cgi-bin/player.cgi?p={player}#splits"
    table_52 = get_second_matching_table(url_52, lambda headers: 'Split' in headers and 'M' in headers and 'W' in headers)
    if table_52:
        output_file = f"splits_results_52weeks2/{player}_splits_52weeks.csv"
        table_to_csv(table_52, player, output_file)


    # RANKINGS
    table_rankings = get_table_from_url(url_splits, lambda headers: 'Year' in headers and 'ATP Rank' in headers)
    if table_rankings:
        output_file = f"rankings_results2/{player}_rankings2.csv"
        table_to_csv(table_rankings, player, output_file)

    # H2H
    url_h2h = f"https://www.tennisabstract.com/cgi-bin/player.cgi?p={player}#head-to-heads-h"
    table_h2h = get_table_from_url(url_h2h, lambda headers: 'Opponent' in headers and 'W' in headers and 'L' in headers)
    if table_h2h:
        output_file = f"h2h_results2/{player}_h2h2.csv"
        table_to_csv(table_h2h, player, output_file)
