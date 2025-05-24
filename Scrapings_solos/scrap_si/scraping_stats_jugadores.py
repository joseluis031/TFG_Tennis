from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def extract_match_table(url):               
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    table = soup.find('table', {'id': 'matches'})
    if not table:
        return None

    rows = table.find_all('tr')
    if not rows:
        return None

    headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]
    data = []
    for row in rows[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
        if cols:
            data.append(cols)

    return pd.DataFrame(data, columns=headers)

# Lista de jugadores (como aparecen en la URL, sin espacios)
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

# Crear carpeta de salida
output_dir = "player_stats"
os.makedirs(output_dir, exist_ok=True)

# Bucle principal
for player in players:
    print(f"\n⏳ Procesando: {player}...")

    base_url = f'https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p={player}&f='
    urls = {
        'serve': base_url + 'ACareerqq',
        'return': base_url + 'ACareerqqr1',
        'raw': base_url + 'ACareerqqw1'
    }

    df_main = extract_match_table(urls['serve'])
    df_return = extract_match_table(urls['return'])
    df_raw = extract_match_table(urls['raw'])

    if df_main is None or df_return is None or df_raw is None:
        print(f"⚠️ Error obteniendo datos de {player}. Puede que el nombre esté mal o no haya datos.")
        continue

    if not (len(df_main) == len(df_return) == len(df_raw)):
        print(f"⚠️ Las tablas de {player} tienen diferente número de filas. No se pueden fusionar.")
        continue

    # Fusionar sin duplicar columnas
    df_final = df_main.copy()
    for df_extra in [df_return, df_raw]:
        for col in df_extra.columns:
            if col not in df_final.columns:
                df_final[col] = df_extra[col]

    # Guardar CSV
    df_final.to_csv(os.path.join(output_dir, f"{player}_matches_full.csv"), index=False)
    print(f"Datos guardados para {player}.")

print("\nTodo listo. Archivos guardados en la carpeta 'player_stats'.")
