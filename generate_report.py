def generate_text_report(comparison, recommendations, name1="Jugador 1", name2="Jugador 2"):
    report = []

    # Introducción
    report.append(f"Informe de análisis estratégico: {name1} vs {name2}\n")

    # Resumen individual de cada jugador
    for name in [name1, name2]:
        report.append(f"--- Perfil de {name} ---")
        stats = comparison[name]

        # Win/Loss
        wl = stats["Win/Loss Ratio"]
        report.append(f"Victorias: {wl['Wins']}, Derrotas: {wl['Losses']}, Ratio de Victorias: {wl['Win Ratio']:.2f}")

        # Mejores superficies
        report.append("Superficies más efectivas (por % de puntos ganados):")
        for surface, vals in stats["Best Surfaces"].items():
            tpw = vals.get("TPW", 0)
            rpw = vals.get("RPW", 0)
            report.append(f"  {surface}: TPW={tpw:.2f}%, RPW={rpw:.2f}%")

        # Dominance Ratio
        report.append(f"Dominance Ratio medio: {stats['Dominance Ratio']:.2f}")

        # Servicio
        report.append("Estadísticas de servicio:")
        for k, v in stats["Service Stats"].items():
            report.append(f"  {k}: {v:.2f}%")

        # Devolución
        report.append("Estadísticas de devolución:")
        for k, v in stats["Return Stats"].items():
            report.append(f"  {k}: {v:.2f}%")

        # Break Points
        report.append("Break points:")
        for k, v in stats["Break Stats"].items():
            report.append(f"  {k}: {v:.2f}")

        # Oponentes frecuentes
        report.append("Oponentes más frecuentes:")
        for opponent, count in stats["Common Opponents"].items():
            report.append(f"  {opponent}: {count} veces")

        report.append("")

    # Recomendaciones estratégicas
    report.append("--- Recomendaciones estratégicas ---")
    for name, rec in recommendations.items():
        report.append(f"{name} debería: {rec}")

    return "\n".join(report)
