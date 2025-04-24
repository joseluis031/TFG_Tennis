import pandas as pd



# Convierte porcentajes, fracciones y decimales a formatos numéricos apropiados
def preprocess_stats(df):
    # Columnas tipo "58.4%" → convertir a float
    percent_cols = ["TPW", "RPW", "A%", "DF%", "1stIn", "1st%", "2nd%", "v1st%", "v2nd%", "vA%"]
    for col in percent_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].str.rstrip('%'), errors='coerce')

    # Dominance Ratio (decimal)
    if "DR" in df.columns:
        df["DR"] = pd.to_numeric(df["DR"], errors="coerce")

    # Fracciones tipo "3/5" → 0.6
    def parse_fraction(val):
        try:
            if isinstance(val, str) and '/' in val:
                num, denom = map(float, val.split('/'))
                return num / denom if denom != 0 else None
        except:
            return None
        return None

    if "BPCnv" in df.columns:
        df["BPCnv"] = df["BPCnv"].apply(parse_fraction)

    if "BPSvd" in df.columns:
        df["BPSvd"] = df["BPSvd"].apply(parse_fraction)

    return df


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

def get_service_stats(df):
    return {
        "1st Serve Points Won %": df["1st%"].mean(),
        "2nd Serve Points Won %": df["2nd%"].mean(),
        "1st Serve In %": df["1stIn"].mean(),
        "Double Fault %": df["DF%"].mean(),
        "Ace %": df["A%"].mean()
    }

# Calcula estadísticas relacionadas con la devolución del jugador
def get_return_stats(df):
    return {
        "Return Points Won (RPW) %": df["RPW"].mean(),
        "v1st% (Rival 1st Serve Won %)": df["v1st%"].mean(),
        "v2nd% (Rival 2nd Serve Won %)": df["v2nd%"].mean(),
        "Opponent Ace Ratio (vA%)": df["vA%"].mean()
    }

# Calcula los promedios de break points convertidos y salvados
def get_break_stats(df):
    return {
        "Break Points Converted": df["BPCnv"].mean(),
        "Break Points Saved": df["BPSvd"].mean()
    }

# Calcula el promedio del Dominance Ratio
def get_dominance_ratio(df):
    return df["DR"].mean()

def summarize_player(df):
    df = preprocess_stats(df)  # Preprocesamos antes de analizar

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

