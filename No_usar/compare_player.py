from No_usar.analyze_player import summarize_player

# Compara dos jugadores usando sus DataFrames y genera un resumen combinado
def compare_players(df1, df2, name1="Jugador 1", name2="Jugador 2"):
    summary1 = summarize_player(df1)
    summary2 = summarize_player(df2)

    comparison = {
        name1: summary1,
        name2: summary2
    }

    strategic_recommendations = generate_recommendations(summary1, summary2, name1, name2)

    return {
        "comparison": comparison,
        "recommendations": strategic_recommendations
    }

# Lógica básica para generar recomendaciones estratégicas comparando estadísticas clave
def generate_recommendations(s1, s2, name1, name2):
    recs = {}

    # Si el segundo servicio del rival es débil, se recomienda atacarlo
    if s2["Service Stats"]["2nd Serve Points Won %"] < 45:
        recs[name1] = f"Aprovechar el segundo servicio de {name2}, que tiene un rendimiento bajo (<45%)."

    # Si el jugador 1 es mejor al resto que el jugador 2
    if s1["Return Stats"]["Return Points Won (RPW) %"] > s2["Return Stats"]["Return Points Won (RPW) %"]:
        recs[name1] = recs.get(name1, "") + f" Tiene mejor desempeño al resto que {name2}, debería presionar más en los juegos de devolución."

    # Si el jugador 1 tiene un Dominance Ratio más alto
    if s1["Dominance Ratio"] > s2["Dominance Ratio"]:
        recs[name1] = recs.get(name1, "") + f" Dominance Ratio superior, puede mantener el control del ritmo de juego."

    # Recomendaciones inversas para el jugador 2
    if s1["Service Stats"]["2nd Serve Points Won %"] < 45:
        recs[name2] = f"Aprovechar el segundo servicio de {name1}, que tiene un rendimiento bajo (<45%)."

    if s2["Return Stats"]["Return Points Won (RPW) %"] > s1["Return Stats"]["Return Points Won (RPW) %"]:
        recs[name2] = recs.get(name2, "") + f" Tiene mejor desempeño al resto que {name1}, debería presionar más en los juegos de devolución."

    if s2["Dominance Ratio"] > s1["Dominance Ratio"]:
        recs[name2] = recs.get(name2, "") + f" Dominance Ratio superior, puede mantener el control del ritmo de juego."

    return recs
