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


# === Diccionarios descriptivos para perfiles ===
dic_saque = {
    's': 'JUGADOR PELIGROSO',
    'a': 'JUGADOR BUENO',
    'b': 'JUGADOR NORMAL'
}

dic_resto = {
    's': 'JUGADOR PELIGROSO',
    'a': 'JUGADOR BUENO AL ',
    'b': 'JUGADOR NORMAL AL RESTO'
}

dic_break_saque = {
    's': 'JUGADOR PELIGROSO EN PUNTOS/JUEGOS CLAVE AL SAQUE',
    'a': 'JUGADOR BUENO EN PUNTOS/JUEGOS CLAVE AL SAQUE',
    'b': 'JUGADOR NORMAL AL RESTO'
}
# === Funciones auxiliares ===
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

# === App Streamlit ===
st.title("🎾 Comparador de Jugadores de Tenis")

df_hard = pd.read_csv("Juego_2024_25/merged_hard.csv")
df_clay = pd.read_csv("Juego_2024_25/merged_clay.csv")
df_perfiles = pd.read_csv("top_10_atp.csv")

superficie = st.selectbox("Selecciona superficie", ["Hard", "Clay"])
df = df_hard if superficie == "Hard" else df_clay

jugadores = sorted(df["Player"].unique())
jug1 = st.selectbox("Jugador 1", jugadores)
jug2 = st.selectbox("Jugador 2", jugadores, index=1)

# Mostrar perfiles
def mostrar_perfil(nombre):
    row = df_perfiles[df_perfiles['Jugador'].str.replace(" ", "").str.lower() == nombre.replace(" ", "").lower()].squeeze()

    st.markdown(f"**Nombre:** {nombre}")
    st.markdown(f"**Nacionalidad:** {row['Nacionality']}")
    st.markdown(f"**Edad:** {row['Age']}")
    st.markdown(f"**Mano:** {row['Hand']}")
    st.markdown(f"**Backhand:** {row['Backhand']}")
    # Mostrar ranking Elo general
    st.markdown(f"**Elo Rank:** {row['Elo Rank']}")

    # Mostrar ranking Elo según superficie
    if superficie == "Clay":
        st.markdown(f"**Elo Rank en Supeficie:** {row['cElo Rank']}")
    elif superficie == "Hard":
        st.markdown(f"**hElo Rank en Superficie:** {row['hElo Rank']}")

    # Elegir columnas dinámicas según la superficie
    sufijo = '_clay' if superficie == "Clay" else ''

    # Obtener los valores correctos según la superficie
    valor_saque = dic_saque.get(row[f'saque{sufijo}'], 'Desconocido')
    valor_resto = dic_saque.get(row[f'resto{sufijo}'], 'Desconocido')
    valor_break_saque = dic_saque.get(row[f'break_saque{sufijo}'], 'Desconocido')
    valor_break_resto = dic_saque.get(row[f'break_resto{sufijo}'], 'Desconocido')

    st.markdown(f"**Nivel Saque:** {valor_saque}")
    st.markdown(f"**Nivel Resto:** {valor_resto}")
    st.markdown(f"**Nivel en puntos/juegos clave al servicio:** {valor_break_saque}")
    st.markdown(f"**Nivel en puntos/juegos clave al resto:** {valor_break_resto}")


# Layout principal: 3 columnas
col1, col2, col3 = st.columns([1.5, 2, 1.5])

# Perfil Jugador 1
with col1:
    st.subheader("👤 Perfil Jugador 1")
    mostrar_perfil(jug1)

with col2:
    st.subheader("📊 Comparaciones")

    df_sel = df[df["Player"].isin([jug1, jug2])].set_index("Player")
    colors = ['#1f77b4', '#ff7f0e']

    # Expander: Comparación Servicio
    with st.expander("Al Servicio"):
        variables = ['2ndAgg', '2nd: Unret%']
        labels_mostrar = ['Agresividad 2º Servicio', '% Saques No Devueltos con 2º servicio']

        for var, label in zip(variables, labels_mostrar):
            x = np.arange(2)
            fig, ax = plt.subplots(figsize=(5, 3.5))
            for i, jugador in enumerate([jug1, jug2]):
                valor = df_sel.loc[jugador, var]
                ax.bar(i, valor, color=colors[i], label=jugador)
            ax.set_xticks(x)
            ax.set_xticklabels([jug1, jug2])
            ax.set_ylabel("Valor")
            ax.set_title(label)
            ax.legend()
            st.pyplot(fig)

# Gráfico 2: Dirección del saque "Wide" (usando jug1 y jug2)
        variables_wide = ['D Wide%', 'A Wide%']
        labels_wide = ['Dirección Wide (Deuce)', 'Dirección Wide (Ad)']

        if all(v in df.columns for v in variables_wide):
            x = np.arange(len(variables_wide))
            width = 0.35
            fig, ax = plt.subplots(figsize=(6, 4))

            for i, jugador in enumerate([jug1, jug2]):
                valores = df_sel.loc[jugador, variables_wide].values
                ax.bar(x + i * width - width / 2, valores, width, label=jugador)

            ax.set_xticks(x)
            ax.set_xticklabels(labels_wide)
            ax.set_ylabel("Porcentaje (%)")
            ax.set_title("Dirección del saque: Wide en Deuce y Ad")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para mostrar la dirección del saque.")

    # Expander: Comparación Rallys
    with st.expander("En Rallys"):
        # Gráfica 1: Duración media del rally
        variables_rally = ['RLen-Serve', 'RLen-Return']
        labels_rally = ['Rally medio al saque', 'Rally medio al resto']
        x = np.arange(len(variables_rally))
        width = 0.35
        fig, ax = plt.subplots(figsize=(6, 4))
        for i, jugador in enumerate([jug1, jug2]):
            valores = df_sel.loc[jugador, variables_rally].values
            ax.bar(x + i * width - width / 2, valores, width, label=jugador)
        ax.set_xticks(x)
        ax.set_xticklabels(labels_rally)
        ax.set_ylabel("Duración media (golpes)")
        ax.set_title("Duración media del rally")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)

        # Gráfica 2: Radar de rallies ganados
        labels_radar = ['1-3 W%', '4-6 W%', '7-9 W%', '10+ W%']
        df_filtrado = df[df['Player'].isin([jug1, jug2])].copy()
        angles = np.linspace(0, 2 * np.pi, len(labels_radar), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        def add_player(ax, row, label):
            values = [row[var] for var in labels_radar] + [row[labels_radar[0]]]
            ax.plot(angles, values, label=label)
            ax.fill(angles, values, alpha=0.25)

        for _, row in df_filtrado.iterrows():
            add_player(ax, row, row['Player'])

        valores_min = df_filtrado[labels_radar].min().min()
        valores_max = df_filtrado[labels_radar].max().max()
        margen = (valores_max - valores_min) * 0.1
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels_radar)
        ax.set_ylim(valores_min - margen, valores_max + margen)
        ax.set_title("Rallies ganados por duración")
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        st.pyplot(fig)

     # Expander: Comparación Táctica
    with st.expander("Variación de Táctica"):
        metricas = ['SnV Freq', 'Drop: Freq']

        if all(m in df.columns for m in metricas):
            df_sel_tac = df[df['Player'].isin([jug1, jug2])].set_index('Player')

            x = np.arange(len(metricas))
            width = 0.35

            fig, ax = plt.subplots(figsize=(6, 5))

            val1 = df_sel_tac.loc[jug1, metricas]
            val2 = df_sel_tac.loc[jug2, metricas]

            ax.bar(x - width/2, val1, width, label=jug1)
            ax.bar(x + width/2, val2, width, label=jug2)

            ax.set_xticks(x)
            ax.set_xticklabels(['Serve & Volley (%)', 'Dropshot Frequency (%)'])
            ax.set_ylabel("Frecuencia (%)")
            ax.set_title("Comparación de variedad táctica: SnV vs Dejada")
            ax.legend(loc='upper right')
            ax.grid(True, linestyle="--", alpha=0.3)

            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para la comparación táctica.")

    # Expander: Juegos y Puntos Clave
    with st.expander("Juegos y Puntos Clave"):
        df_filtrado = df[df['Player'].isin([jug1, jug2])].copy()

        # Radar Chart: SvForSet, SvStaySet, SvForMatch, SvStayMatch
        labels_radar = ['SvForSet', 'SvStaySet', 'SvForMatch', 'SvStayMatch']
        if all(label in df.columns for label in labels_radar):
            angles = np.linspace(0, 2 * np.pi, len(labels_radar), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

            def add_player(ax, row, label):
                values = [row[var] for var in labels_radar]
                values += values[:1]
                ax.plot(angles, values, label=label)
                ax.fill(angles, values, alpha=0.25)

            for _, row in df_filtrado.iterrows():
                add_player(ax, row, row['Player'])

            valores_min = df_filtrado[labels_radar].min().min()
            valores_max = df_filtrado[labels_radar].max().max()
            margen = (valores_max - valores_min) * 0.1

            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            ax.set_thetagrids(np.degrees(angles[:-1]), labels_radar)
            ax.set_title("Comparación de desempeño en juegos clave")
            ax.set_ylim(valores_min - margen, valores_max + margen)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para el radar de juegos clave.")

        # Gráfico de barras: BreakBack% y Consol%
        metricas_clave = ['BreakBack%', 'Consol%']
        if all(m in df.columns for m in metricas_clave):
            df_sel_clave = df[df['Player'].isin([jug1, jug2])].set_index('Player')

            x = np.arange(len(metricas_clave))
            width = 0.35
            fig, ax = plt.subplots(figsize=(6, 5))

            val1 = df_sel_clave.loc[jug1, metricas_clave]
            val2 = df_sel_clave.loc[jug2, metricas_clave]

            ax.bar(x - width/2, val1, width, label=jug1)
            ax.bar(x + width/2, val2, width, label=jug2)

            ax.set_xticks(x)
            ax.set_xticklabels(['BreakBack%', 'Consol%'])
            ax.set_ylabel("Porcentaje (%)")
            ax.set_title("Comparación mental: recuperación vs consolidación")
            ax.legend(loc='lower right')
            ax.grid(True, linestyle="--", alpha=0.3)

            st.pyplot(fig)
        else:
            st.warning("Faltan columnas para la comparación mental.")

    # Expander: Winners y Errores No Forzados
    with st.expander("Winners y Errores No Forzados"):
        df_filtrado = df[df['Player'].isin([jug1, jug2])].set_index('Player')

        grupos = [
            (['Wnr/Pt', 'UFE/Pt'], ['Winners por punto', 'Errores no forzados por punto']),
            (['vs Wnr/Pt', 'vs UFE/Pt'], ['Winners recibidos por punto', 'Errores forzados al rival por punto'])
        ]

        width = 0.35

        for vars_, labels in grupos:
            if all(v in df.columns for v in vars_):
                x = np.arange(len(vars_))
                fig, ax = plt.subplots(figsize=(6, 4))

                for i, jugador in enumerate([jug1, jug2]):
                    valores = df_filtrado.loc[jugador, vars_].values
                    ax.bar(x + i * width - width / 2, valores, width, label=jugador)

                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=15)
                ax.set_ylabel("Valor")
                ax.set_title("Comparación táctica")
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.3)

                st.pyplot(fig)
            else:
                st.warning(f"Faltan columnas: {', '.join([v for v in vars_ if v not in df.columns])}")

    # Historial H2H
    if st.button("📊 Mostrar historial H2H"):
        nombre1 = convertir_nombre(jug1)
        nombre2 = convertir_nombre(jug2)
        h2h = obtener_h2h_streamlit(nombre1, nombre2)
        if h2h is not None:
            st.subheader("📋 Historial H2H:")
            st.dataframe(h2h)
        else:
            st.warning("❗ No se pudo obtener el historial H2H.")

# Perfil Jugador 2
with col3:
    st.subheader("👤 Perfil Jugador 2")
    mostrar_perfil(jug2)