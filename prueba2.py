from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

# === Lista de jugadores ===
player = [
    'Jannik Sinner', 'Carlos Alcaraz', 'Novak Djokovic', 'Daniil Medvedev',
    'Alexander Zverev', 'Stefanos Tsitsipas', 'Andrey Rublev', 'Casper Ruud',
    'Hubert Hurkacz', 'Holger Rune'
]

# === Mostrar jugadores y pedir selección ===
for i, p in enumerate(player, 1):
    print(f"{i}. {p}")
choice1 = int(input("Jugador 1 (número): ")) - 1
choice2 = int(input("Jugador 2 (número): ")) - 1
player1 = player[choice1]
player2 = player[choice2]

# === URL de MatchStat H2H ===
url = f"https://matchstat.com/tennis/h2h-odds-bets/{quote(player1)}/{quote(player2)}"

# === Configurar navegador ===
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")
# options.add_argument("--headless")  # Descomenta para modo invisible
driver = webdriver.Chrome(options=options)

try:
    print(f"Accediendo a: {url}")
    driver.get(url)

    # Esperar a que cargue el contenido
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "H2hPlayerInfo"))
    )

    soup = BeautifulSoup(driver.page_source, "lxml")

    # Buscar div y luego la tabla dentro
    container = soup.find("div", id="H2hPlayerInfo")
    table = container.find("table")

    if not table:
        raise ValueError("No se encontró la tabla dentro del div 'H2hPlayerInfo'.")

    data = []
    for row in table.find_all("tr", class_="row_st"):
        cells = row.find_all("td")
        if len(cells) == 3:
            val1 = cells[0].get_text(strip=True)
            label = cells[1].get_text(strip=True)
            val2 = cells[2].get_text(strip=True)
            data.append([label, val1, val2])

    if data:
        df = pd.DataFrame(data, columns=["Estadística", player1, player2])
        print(df)
        # df.to_csv(f"h2h_{player1.replace(' ', '')}_vs_{player2.replace(' ', '')}.csv", index=False)
        # print("Historial H2H guardado correctamente.")
    # else:
        # print("No se encontraron estadísticas válidas.")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
