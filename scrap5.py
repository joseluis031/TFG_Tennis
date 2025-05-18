
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time
import os




# def aplicar_filtro_y_extraer_tablas_completas(filtro_surface: str, output_path: str):
#     options = Options()
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(options=options)

#     try:
#         url = "https://www.tennisabstract.com/cgi-bin/leaders.cgi?players=51-100"
#         driver.get(url)

#         # Aplicar filtro de superficie
#         WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "surfacehead")))
#         driver.find_element(By.ID, "surfacehead").click()
#         time.sleep(1)

#         filtro_id_map = {
#             "Grass": "surface2",
#             "Clay": "surface1",
#             "Hard": "surface0",
#         }

#         filtro_id = filtro_id_map.get(filtro_surface)
#         if not filtro_id:
#             print(f"Filtro '{filtro_surface}' no reconocido.")
#             return

#         driver.find_element(By.ID, filtro_id).click()
#         time.sleep(4)

#         # Botones de pestañas
#         pestañas = {
#             "Serve": "statso",
#             "Return": "statsw",
#             "Breaks": "statsl",
#             "More": "statst"
#         }

#         tablas = []
#         for nombre, clase in pestañas.items():
#             print(f"Extrayendo: {nombre}")
#             # Click en la pestaña
#             driver.find_element(By.CLASS_NAME, clase).click()
#             time.sleep(3)

#             soup = BeautifulSoup(driver.page_source, 'lxml')
#             table = soup.find("table", {"id": "matches"})
#             if table:
#                 rows = table.find_all("tr")
#                 data = []
#                 for row in rows:
#                     cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
#                     if cols:
#                         data.append(cols)

#                 headers = data[0]
#                 data_rows = data[1:]
#                 df = pd.DataFrame(data_rows, columns=headers)
#                 tablas.append(df)
#             else:
#                 print(f"No se encontró la tabla para {nombre}")

#         # Combinación horizontal de las tablas
#         df_final = pd.concat(tablas, axis=1)
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         df_final.to_csv(output_path, index=False, encoding="utf-8-sig")
#         print(f"Archivo combinado guardado en: {output_path}")

#     except TimeoutException:
#         print("Tiempo de espera agotado.")
#     except Exception as e:
#         print(f"Error inesperado: {e}")
#     finally:
#         driver.quit()

# # Ejemplo de uso
# if __name__ == "__main__":
#     aplicar_filtro_y_extraer_tablas_completas("Grass", "output/tabla_completa_grass.csv")

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# import os

# def extraer_tabla_completa(driver, filtro_surface: str, url: str):
#     driver.get(url)

#     WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "surfacehead")))
#     driver.find_element(By.ID, "surfacehead").click()
#     time.sleep(1)

#     filtro_id_map = {
#         "Grass": "surface2",
#         "Clay": "surface1",
#         "Hard": "surface0",
#     }

#     filtro_id = filtro_id_map.get(filtro_surface)
#     if not filtro_id:
#         raise ValueError(f"Filtro '{filtro_surface}' no reconocido.")

#     driver.find_element(By.ID, filtro_id).click()
#     time.sleep(3)

#     pestañas = {
#         "Serve": "statso",
#         "Return": "statsw",
#         "Breaks": "statsl",
#         "More": "statst"
#     }

#     tablas = []
#     for nombre, clase in pestañas.items():
#         driver.find_element(By.CLASS_NAME, clase).click()
#         time.sleep(2)
#         soup = BeautifulSoup(driver.page_source, 'lxml')
#         table = soup.find("table", {"id": "matches"})
#         if table:
#             rows = table.find_all("tr")
#             data = []
#             for row in rows:
#                 cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
#                 if cols:
#                     data.append(cols)
#             headers = data[0]
#             data_rows = data[1:]
#             df = pd.DataFrame(data_rows, columns=headers)
#             tablas.append(df)
#         else:
#             print(f"No se encontró la tabla {nombre}")

#     # Concatenación horizontal de pestañas
#     df_final = pd.concat(tablas, axis=1)
#     return df_final


# def scrapear_todas_tablas_y_guardar(filtro_surface: str, output_path: str):
#     options = Options()
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(options=options)

#     try:
#         urls = [
#             "https://www.tennisabstract.com/cgi-bin/leaders.cgi",
#             "https://www.tennisabstract.com/cgi-bin/leaders.cgi?players=51-100"
#         ]

#         bloques = []
#         for url in urls:
#             print(f"Procesando: {url}")
#             bloque = extraer_tabla_completa(driver, filtro_surface, url)
#             bloque = bloque.iloc[:-1]  # Eliminar la última fila
#             bloques.append(bloque)

#         # Unir verticalmente por filas
#         df_completo = pd.concat(bloques, axis=0).reset_index(drop=True)

#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         df_completo.to_csv(output_path, index=False, encoding="utf-8-sig")
#         print(f"Dataset combinado guardado en: {output_path}")

#     except Exception as e:
#         print(f"Error inesperado: {e}")
#     finally:
#         driver.quit()


# # Uso
# if __name__ == "__main__":
#     scrapear_todas_tablas_y_guardar("Grass", "output/stats_top_100_grass.csv")


# def extraer_estadisticas_2024_hard(output_path):
#     urls = [
#         "https://www.tennisabstract.com/cgi-bin/leaders.cgi",
#         "https://www.tennisabstract.com/cgi-bin/leaders.cgi?players=51-100"
#     ]

#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--disable-gpu')
#     driver = webdriver.Chrome(options=chrome_options)

#     try:
#         tablas_totales = []

#         for url in urls:
#             driver.get(url)
#             WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanhead")))

#             # Filtro año 2024
#             driver.find_element(By.ID, "spanhead").click()
#             time.sleep(0.5)
#             driver.find_element(By.ID, "span2024qq").click()
#             time.sleep(2)

#             # Filtro superficie Hard
#             driver.find_element(By.ID, "surfacehead").click()
#             time.sleep(0.5)
#             driver.find_element(By.ID, "surface0").click()
#             time.sleep(3)

#             # Stats: Serve, Return, Breaks, More
#             secciones_stats = ["statso", "statsw", "statsl", "statst"]
#             df_combinado = None

#             for stat_id in secciones_stats:
#                 try:
#                     driver.find_element(By.CLASS_NAME, stat_id).click()
#                     time.sleep(2)

#                     soup = BeautifulSoup(driver.page_source, 'lxml')
#                     tabla = soup.find("table", {"id": "matches"})

#                     if tabla:
#                         rows = tabla.find_all("tr")
#                         data = []
#                         for row in rows:
#                             cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
#                             if cols:
#                                 data.append(cols)
#                         if not data:
#                             continue
#                         headers = data[0]
#                         data_rows = data[1:-1]  # Quitamos la última fila (promedio)

#                         df = pd.DataFrame(data_rows, columns=headers)

#                         if df_combinado is None:
#                             df_combinado = df
#                         else:
#                             df_combinado = df_combinado.merge(df, on="Rk", suffixes=("", "_dup"), how="left")

#                 except Exception as e:
#                     print(f"Error en sección {stat_id}: {e}")

#             if df_combinado is not None:
#                 tablas_totales.append(df_combinado)

#         # Concatenar verticalmente: top 50 + top 51-100
#         df_final = pd.concat(tablas_totales, axis=0, ignore_index=True)
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         df_final.to_csv(output_path, index=False, encoding="utf-8-sig")
#         print(f"Datos guardados en: {output_path}")

#     finally:
#         driver.quit()

# # Ejecutar
# extraer_estadisticas_2024_hard("output/estadisticas_2024_hard.csv")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def extraer_estadisticas_por_torneo(torneo_id: str, torneo_nombre: str, output_path: str):
    urls = [
        "https://www.tennisabstract.com/cgi-bin/leaders.cgi",
        "https://www.tennisabstract.com/cgi-bin/leaders.cgi?players=51-100"
    ]

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        tablas_totales = []

        for url in urls:
            driver.get(url)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanhead")))

            # Filtro año 2024
            driver.find_element(By.ID, "spanhead").click()
            time.sleep(0.5)
            driver.find_element(By.ID, "span2024qq").click()
            time.sleep(2)

            # Filtro de torneo (Level)
            driver.find_element(By.ID, "levelhead").click()
            time.sleep(0.5)
            driver.find_element(By.ID, torneo_id).click()
            time.sleep(3)

            # Stats: Serve, Return, Breaks, More
            secciones_stats = ["statso", "statsw", "statsl", "statst"]
            df_combinado = None

            for stat_id in secciones_stats:
                try:
                    driver.find_element(By.CLASS_NAME, stat_id).click()
                    time.sleep(2)

                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    tabla = soup.find("table", {"id": "matches"})

                    if tabla:
                        rows = tabla.find_all("tr")
                        data = []
                        for row in rows:
                            cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
                            if cols:
                                data.append(cols)
                        if not data:
                            continue
                        headers = data[0]
                        data_rows = data[1:-1]  # Quitar última fila

                        df = pd.DataFrame(data_rows, columns=headers)

                        if df_combinado is None:
                            df_combinado = df
                        else:
                            df_combinado = df_combinado.merge(df, on="Rk", suffixes=("", "_dup"), how="left")

                except Exception as e:
                    print(f"Error en sección {stat_id} para torneo {torneo_nombre}: {e}")

            if df_combinado is not None:
                tablas_totales.append(df_combinado)

        # Concatenar verticalmente
        df_final = pd.concat(tablas_totales, axis=0, ignore_index=True)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_final.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"[✓] Datos guardados para torneo '{torneo_nombre}' en: {output_path}")

    finally:
        driver.quit()


# Bucle para recorrer tipos de torneo
niveles_torneo = {
    "level0": "GrandSlams",
    "level1": "Masters"
}

for torneo_id, nombre in niveles_torneo.items():
    ruta_salida = f"output2/estadisticas_2024_{nombre}.csv"
    extraer_estadisticas_por_torneo(torneo_id, nombre, ruta_salida)
