import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

# --- Función para convertir nombres tipo CarlosAlcaraz a Carlos Alcaraz
def convertir_nombre(nombre):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', nombre)

# --- Función para scraping H2H desde MatchStat
def obtener_h2h_streamlit(player1, player2):
    st.info("🔍 Accediendo a MatchStat para obtener H2H...")
    url = f"https://matchstat.com/tennis/h2h-odds-bets/{quote(player1)}/{quote(player2)}"
    st.markdown(f"🌐 URL: [Abrir MatchStat]({url})")

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "H2hPlayerInfo"))
        )
        soup = BeautifulSoup(driver.page_source, "lxml")
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
                if label not in ["Career Prize Money", "YTD Titles"]:
                    data.append([label, val1, val2])

        if data:
            df = pd.DataFrame(data, columns=["Estadística", player1, player2])
            return df

    except Exception as e:
        st.error(f"❌ Error al extraer datos: {e}")
        return None

    finally:
        driver.quit()

# --- Streamlit App ---
st.title("🎾 Comparador de Jugadores + Historial H2H")

# --- Cargar CSVs ---
df_hard = pd.read_csv("Juego_2024_25/merged_hard.csv")
df_clay = pd.read_csv("Juego_2024_25/merged_clay.csv")

# --- Selección dataset ---
surface = st.selectbox("Selecciona superficie", ["Hard", "Clay"])
df = df_hard if surface == "Hard" else df_clay

# --- Selección de jugadores ---
jugadores = sorted(df["Player"].unique())
jug1 = st.selectbox("Jugador 1", jugadores)
jug2 = st.selectbox("Jugador 2", jugadores, index=1)

# --- Mostrar comparación de stats rápidas ---
variables = ['2ndAgg', '2nd: Unret%']
labels_mostrar = ['Agresividad 2º Servicio', '% Saques No Devueltos con 2º servicio']
df_sel = df[df["Player"].isin([jug1, jug2])].set_index("Player")
colors = ['#1f77b4', '#ff7f0e']

for var, label in zip(variables, labels_mostrar):
    x = np.arange(2)
    fig, ax = plt.subplots(figsize=(6, 4))
    for i, jugador in enumerate([jug1, jug2]):
        valor = df_sel.loc[jugador, var]
        ax.bar(i, valor, color=colors[i], label=jugador)

    ax.set_xticks(x)
    ax.set_xticklabels([jug1, jug2])
    ax.set_ylabel("Valor")
    ax.set_title(label)
    ax.legend()
    st.pyplot(fig)

# --- Botón para mostrar H2H ---
if st.button("📊 Mostrar historial H2H"):
    nombre1 = convertir_nombre(jug1)
    nombre2 = convertir_nombre(jug2)
    h2h = obtener_h2h_streamlit(nombre1, nombre2)
    if h2h is not None:
        st.subheader("📋 Historial H2H:")
        st.dataframe(h2h)
    else:
        st.warning("❗ No se pudo mostrar el historial.")
