import streamlit as st

dic_saque = {'s': 'JUGADOR PELIGROSO', 'a': 'JUGADOR BUENO', 'b': 'JUGADOR NORMAL'}
dic_resto = {'s': 'JUGADOR PELIGROSO', 'a': 'JUGADOR BUENO AL', 'b': 'JUGADOR NORMAL AL RESTO'}
dic_break_saque = {'s': 'JUGADOR PELIGROSO EN PUNTOS/JUEGOS CLAVE AL SAQUE',
                   'a': 'JUGADOR BUENO EN PUNTOS/JUEGOS CLAVE AL SAQUE',
                   'b': 'JUGADOR NORMAL AL RESTO'}

def mostrar_perfil(nombre, df_perfiles, superficie):
    row = df_perfiles[df_perfiles['Jugador'].str.replace(" ", "").str.lower() == nombre.replace(" ", "").lower()].squeeze()

    st.markdown(f"**Nacionalidad:** {row['Nacionality']}")
    st.markdown(f"**Edad:** {row['Age']}")
    st.markdown(f"**Mano:** {row['Hand']}")
    st.markdown(f"**Backhand:** {row['Backhand']}")
    st.markdown(f"**Elo Rank:** {row['Elo Rank']}")

    if superficie == "Clay":
        st.markdown(f"**Elo Rank en Superficie:** {row['cElo Rank']}")
    elif superficie == "Hard":
        st.markdown(f"**Elo Rank en Superficie:** {row['hElo Rank']}")

    sufijo = '_clay' if superficie == "Clay" else ''
    st.markdown(f"**Nivel Saque:** {dic_saque.get(row[f'saque{sufijo}'], 'Desconocido')}")
    st.markdown(f"**Nivel Resto:** {dic_saque.get(row[f'resto{sufijo}'], 'Desconocido')}")
    st.markdown(f"**Nivel en puntos/juegos clave al servicio:** {dic_saque.get(row[f'break_saque{sufijo}'], 'Desconocido')}")
    st.markdown(f"**Nivel en puntos/juegos clave al resto:** {dic_saque.get(row[f'break_resto{sufijo}'], 'Desconocido')}")
