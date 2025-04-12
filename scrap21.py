from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

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
    headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]
    data = []

    for row in rows[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
        if cols:
            data.append(cols)

    return pd.DataFrame(data, columns=headers)

# URLs para Jannik Sinner
base_url = 'https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p=JannikSinner&f='
urls = {
    'serve': base_url + 'ACareerqq',
    'return': base_url + 'ACareerqqr1',
    'raw': base_url + 'ACareerqqw1'
}

# Extraer tablas
df_main = extract_match_table(urls['serve'])
df_return = extract_match_table(urls['return'])
df_raw = extract_match_table(urls['raw'])

# Validar que tienen la misma cantidad de filas
if not (len(df_main) == len(df_return) == len(df_raw)):
    raise ValueError("⚠️ Las tablas no tienen el mismo número de filas. No se puede fusionar correctamente.")

# Eliminar columnas duplicadas al combinar
df_final = df_main.copy()

# Agregar columnas únicas de cada uno
for df_extra in [df_return, df_raw]:
    for col in df_extra.columns:
        if col not in df_final.columns:
            df_final[col] = df_extra[col]

# Guardar el resultado final
df_final.to_csv("sinner_matches_full.csv", index=False)
print("✅ Datos combinados guardados en sinner_matches_full.csv")
