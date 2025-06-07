import streamlit as st

def get_mean_elo(player_name, df_perfiles, surface):
    row = df_perfiles[df_perfiles['Jugador'].str.replace(" ", "").str.lower() == player_name.replace(" ", "").lower()]
    if row.empty:
        return None
    if surface == "Hard":
        return row[['Elo', 'hElo']].mean(axis=1).values[0]
    elif surface == "Clay":
        return row[['Elo', 'cElo']].mean(axis=1).values[0]
    return None

def calcular_probabilidad_victoria(mean1, mean2):
    diff = mean1 - mean2
    return 1 - (1 / (1 + (10 ** (diff / 400))))

def mostrar_probabilidad(jug1, jug2, df_perfiles, superficie):
    media1 = get_mean_elo(jug1, df_perfiles, superficie)
    media2 = get_mean_elo(jug2, df_perfiles, superficie)

    if media1 is not None and media2 is not None:
        prob = calcular_probabilidad_victoria(media1, media2)
        st.markdown("---")
        st.subheader("📈 Probabilidad de victoria según Ranking ELO")
        st.markdown(f"**Probabilidad de que {jug1} gane contra {jug2} en {superficie}:** `{prob:.2%}`")
    else:
        st.warning("No se pudo calcular la probabilidad porque faltan datos.")
