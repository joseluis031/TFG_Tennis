import pandas as pd

# Agrupa los partidos por superficie y calcula el promedio de TPW y RPW
def get_surface_performance(df):
    surface_stats = df.groupby("Surface")[["TPW", "RPW"]].mean()
    return surface_stats.sort_values(by="TPW", ascending=False)

# Calcula la cantidad de victorias, derrotas y el ratio de victorias
def get_win_loss_ratio(df):
    wins = df[df["W_or_L"] == "W"].shape[0]
    losses = df[df["W_or_L"] == "L"].shape[0]
    return {
        "Wins": wins,
        "Losses": losses,
        "Win Ratio": wins / (wins + losses) if (wins + losses) > 0 else 0
    }

# Identifica los rivales más comunes enfrentados
def get_common_opponents(df, top_n=5):
    opponents = df["match"].str.extract(r"(.*)\[")[0].fillna(df["match"])
    return opponents.value_counts().head(top_n)

# Calcula estadísticas relacionadas con el servicio del jugador
def get_service_stats(df):
    return {
        "1st Serve Points Won %": df["1st%"].str.rstrip('%').astype(float).mean(),
        "2nd Serve Points Won %": df["2nd%"].str.rstrip('%').astype(float).mean(),
        "1st Serve In %": df["1stIn"].str.rstrip('%').astype(float).mean(),
        "Double Fault %": df["DF%"].str.rstrip('%').astype(float).mean(),
        "Ace %": df["A%"].str.rstrip('%').astype(float).mean()
    }

# Calcula estadísticas relacionadas con la devolución del jugador
def get_return_stats(df):
    return {
        "Return Points Won (RPW) %": df["RPW"].str.rstrip('%').astype(float).mean(),
        "v1st% (Rival 1st Serve Won %)": df["v1st%"].str.rstrip('%').astype(float).mean(),
        "v2nd% (Rival 2nd Serve Won %)": df["v2nd%"].str.rstrip('%').astype(float).mean(),
        "Opponent Ace Ratio (vA%)": df["vA%"].str.rstrip('%').astype(float).mean()
    }

# Calcula los promedios de break points convertidos y salvados
def get_break_stats(df):
    def parse_fraction(series):
        return series.dropna().apply(lambda x: eval(x) if isinstance(x, str) and '/' in x else None)
    return {
        "Break Points Converted": parse_fraction(df["BPCnv"]).mean(),
        "Break Points Saved": parse_fraction(df["BPSvd"]).mean()
    }

# Calcula el promedio del Dominance Ratio
def get_dominance_ratio(df):
    return df["DR"].astype(float).mean()

# Resumen completo del jugador combinando todos los análisis anteriores
def summarize_player(df):
    summary = {
        "Win/Loss Ratio": get_win_loss_ratio(df),
        "Best Surfaces": get_surface_performance(df).to_dict(),
        "Service Stats": get_service_stats(df),
        "Return Stats": get_return_stats(df),
        "Break Stats": get_break_stats(df),
        "Dominance Ratio": get_dominance_ratio(df),
        "Common Opponents": get_common_opponents(df).to_dict()
    }
    return summary
