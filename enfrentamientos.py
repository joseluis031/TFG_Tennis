from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import pandas as pd
import streamlit as st

def mostrar_enfrentamientos(jug1, jug2, df):
    df_sel = df[df["Player"].isin([jug1, jug2])].set_index("Player")
    colors = ['#1f77b4', '#ff7f0e']

def convertir_nombre(nombre):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', nombre)

def obtener_h2h_streamlit(player1, player2):
    url = f"https://matchstat.com/tennis/h2h-odds-bets/{quote(player1)}/{quote(player2)}"
    st.markdown(f"🌐 Accediendo a: [MatchStat H2H]({url})")

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
            excluir = ["Age", "Plays", "Career Total W/L"]
            df = df[~df["Estadística"].isin(excluir)]
            return df
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None
    finally:
        driver.quit()
