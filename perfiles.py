import streamlit as st
import os
from PIL import Image

dic_saque = {'s': 'JUGADOR PELIGROSO', 'a': 'JUGADOR BUENO', 'b': 'JUGADOR NORMAL'}

def mostrar_perfil(nombre, df_perfiles, superficie):
    row = df_perfiles[df_perfiles['Jugador'].str.replace(" ", "").str.lower() == nombre.replace(" ", "").lower()].squeeze()

    # === Mostrar imagen del jugador con tamaño uniforme ===
    ruta_imagen = f"imagenes_perfil/{nombre}.png"
    if os.path.exists(ruta_imagen):
        try:
            img = Image.open(ruta_imagen)

            # Paso 1: Escalado proporcional → lado más corto = 240 px
            target_size = 240
            width, height = img.size
            scale = target_size / min(width, height)
            new_size = (int(width * scale), int(height * scale))
            img_resized = img.resize(new_size, Image.LANCZOS)

            # Paso 2: Recorte centrado 240x240
            left = (img_resized.width - target_size) // 2
            top = (img_resized.height - target_size) // 2
            right = left + target_size
            bottom = top + target_size
            img_cropped = img_resized.crop((left, top, right, bottom))

            st.image(img_cropped)
        except Exception as e:
            st.warning(f"Error al cargar imagen: {e}")
    else:
        st.warning("📸 Imagen no disponible")

    # === Mostrar datos del perfil ===
    st.markdown(f"**Nacionalidad:** {row['Nacionality']}")
    st.markdown(f"**Edad:** {row['Age']}")
    st.markdown(f"**Mano:** {row['Hand']}")
    st.markdown(f"**Backhand:** {row['Backhand']}")
    st.markdown(f"**Elo Rank:** {row['Elo Rank']}")

    if superficie == "Clay":
        st.markdown(f"**Elo Rank en Superficie:** {row['cElo Rank']}")
    elif superficie == "Hard":
        st.markdown(f"**hElo Rank en Superficie:** {row['hElo Rank']}")

    sufijo = '_clay' if superficie == "Clay" else ''
    st.markdown(f"**Nivel Saque:** {dic_saque.get(row[f'saque{sufijo}'], 'Desconocido')}")
    st.markdown(f"**Nivel Resto:** {dic_saque.get(row[f'resto{sufijo}'], 'Desconocido')}")
    st.markdown(f"**Nivel en puntos/juegos clave al servicio:** {dic_saque.get(row[f'break_saque{sufijo}'], 'Desconocido')}")
    st.markdown(f"**Nivel en puntos/juegos clave al resto:** {dic_saque.get(row[f'break_resto{sufijo}'], 'Desconocido')}")
