# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import pandas as pd
# from urllib.parse import quote

# #lista de jugadores para que aparezca en pantalla y elegir

# player= [
#     'Jannik Sinner',   
#     'Carlos Alcaraz',
#     'Novak Djokovic',
#     'Daniil Medvedev',
#     'Alexander Zverev',
#     'Stefanos Tsitsipas',
#     'Andrey Rublev',
#     'Casper Ruud',
#     'Hubert Hurkacz',
#     'Holger Rune'
# ]
# # Mostrar lista de jugadores
# print("Jugadores disponibles:")
# for i, p in enumerate(player, start=1):
#     print(f"{i}. {p}")

# # Entrada por consola para elegir jugadores
# print("Selecciona dos jugadores de la lista (1-10):")
# # Entrada por consola para elegir jugadores
# try:
#     choice1 = int(input("Jugador 1 (número): ")) - 1
#     choice2 = int(input("Jugador 2 (número): ")) - 1

#     if choice1 < 0 or choice1 >= len(player) or choice2 < 0 or choice2 >= len(player):
#         raise ValueError("Selección inválida. Debes elegir números entre 1 y 10.")

#     player1 = player[choice1]
#     player2 = player[choice2]


# except ValueError as e:
#     print(f"Error en la selección: {e}")
#     exit()

# # URL codificada
# url = f"https://matchstat.com/tennis/h2h-odds-bets/{quote(player1)}/{quote(player2)}"

# # Configurar navegador para no mostrar la ventana
# options = Options()
# # options.add_argument('--headless')  # Ejecutar en modo headless
# options.add_argument('--disable-gpu')  # Desactivar GPU para evitar problemas en algunos sistemas
# options.add_argument('--no-sandbox')  # Evitar problemas de sandboxing
# options.add_argument('--window-size=1920x1080')  # Tamaño de ventana para evitar problemas de visualización
# driver = webdriver.Chrome(options=options)


# try:
#     print(f"Abriendo URL: {url}")
#     driver.get(url)

#     # Esperar a que aparezca alguna tabla
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "table"))
#     )

#     soup = BeautifulSoup(driver.page_source, "lxml")
#     tables = soup.find_all("table")

#     if not tables:
#         print("No se encontraron tablas.")
#     else:
#         target_table = tables[0]  # Primera tabla (H2H)

#         rows = target_table.find_all("tr")
#         data = []
#         for row in rows:
#             cols = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
#             if cols:
#                 data.append(cols)

#         df = pd.DataFrame(data[1:], columns=data[0])
#         print("Tabla extraída:")
#         print(df)

#         output_path = f"h2h_{player1.replace(' ', '')}_vs_{player2.replace(' ', '')}.csv"
#         #df.to_csv(output_path, index=False)
#         print(f"Guardado en: {output_path}")

# except Exception as e:
#     print("Error:", e)

# finally:
#     driver.quit()

#quiero copiar un notebook y duplicarlo con otro nombre
import shutil
import os
# Ruta del notebook original
notebook_path = "prueba_copia3.ipynb"  # Cambia esto al nombre de tu notebook original
# Ruta del nuevo notebook
new_notebook_path = "prueba_copia32.ipynb"  # Cambia esto al nombre que desees para la copia
# Verificar si el notebook original existe
if os.path.exists(notebook_path):
    # Copiar el notebook
    shutil.copy(notebook_path, new_notebook_path)
    print(f"Notebook copiado a {new_notebook_path}")