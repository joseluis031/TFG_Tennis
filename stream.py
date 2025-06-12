# stream.py
import streamlit as st
import pandas as pd
import re
from perfiles import mostrar_perfil
from enfrentamientos import mostrar_enfrentamientos, convertir_nombre, obtener_h2h_streamlit
from comparativa import mostrar_comparativas
from pred_elo import mostrar_probabilidad
from agente_llm import generar_analisis_llm

st.set_page_config(page_title="Comparador de Tenis", layout="wide")
st.title("🎾 Informe Pre-partido con Inteligencia Artificial")

# === Utilidad para separar nombre y apellido ===
def separar_nombre(nombre):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', nombre)

# Cargar datasets
df_hard = pd.read_csv("Juego_2024_25/merged_hard.csv")
df_clay = pd.read_csv("Juego_2024_25/merged_clay.csv")
df_perfiles = pd.read_csv("top_10_atp.csv")

# Selección de superficie y jugadores
superficie = st.selectbox("Selecciona superficie", ["Hard", "Clay"])
df = df_hard if superficie == "Hard" else df_clay

jugadores_raw = sorted(df["Player"].unique())
jugadores = [separar_nombre(j) for j in jugadores_raw]

jug1 = st.selectbox("Jugador 1", jugadores)
jug2 = st.selectbox("Jugador 2", jugadores, index=1)

# Convertir de nuevo a nombres sin espacio para acceder a los datos
nombre1 = jug1.replace(" ", "")
nombre2 = jug2.replace(" ", "")

# Layout de columnas
col1, col2, col3 = st.columns([1.5, 2, 1.5])

with col1:
    st.subheader(f"👤 Perfil: {jug1}")
    mostrar_perfil(nombre1, df_perfiles, superficie)

with col2:
    st.subheader("📊 Comparaciones")
    mostrar_enfrentamientos(nombre1, nombre2, df)
    mostrar_comparativas(nombre1, nombre2, df)

    # Historial H2H desde MatchStat
    if st.button("📊 Mostrar historial H2H"):
        nombre1_web = convertir_nombre(nombre1)
        nombre2_web = convertir_nombre(nombre2)
        h2h = obtener_h2h_streamlit(nombre1_web, nombre2_web)
        if h2h is not None:
            st.subheader("📋 Historial H2H:")
            st.dataframe(h2h)
        else:
            st.warning("❗ No se pudo obtener el historial H2H.")

with col3:
    st.subheader(f"👤 Perfil: {jug2}")
    mostrar_perfil(nombre2, df_perfiles, superficie)

# Mostrar probabilidad al final
mostrar_probabilidad(jug1, jug2, df_perfiles, superficie)

df_llm = pd.read_csv("Limpios_llm/Juego_2024_25/merged_hard.csv")  # Asegúrate que coincida con los nombres usados en `jug1` y `jug2`

st.markdown("## 🧠 Informe táctico generado por IA")

if nombre1 != nombre2:
    if st.button("🔍 Generar informe profesional con LLM"):
        with st.spinner("Generando informe... esto puede tardar unos minutos..."):
            resultado = generar_analisis_llm(nombre1, nombre2, df_llm)
            st.markdown("### 📝 Informe:")
            st.write(resultado)
else:
    st.warning("⚠️ Debes elegir dos jugadores diferentes.")