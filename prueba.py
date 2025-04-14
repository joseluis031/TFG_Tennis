import pandas as pd
import re

# Cargar CSV
df = pd.read_csv('Tests/player_stats/AlexanderZverev_matches_full.csv')

def clean_set_score(set_str):
    """Extrae el resultado de un set en formato int-int, eliminando tiebreaks y texto."""
    set_str = re.sub(r'\(.*?\)', '', set_str)  # elimina tiebreaks: (4), (7-5), etc.
    set_str = set_str.replace('ch', '')  # elimina 'ch'
    if '-' not in set_str:
        return None
    parts = set_str.strip().split('-')
    if len(parts) != 2:
        return None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None

def get_winner(row):
    match = str(row['match'])
    score = str(row['Score'])

    # Revisar si el match tiene la forma esperada
    if 'd.' not in match:
        return None

    # Dividir en jugador 1 y 2
    parts = match.split('d.')
    if len(parts) != 2:
        return None

    player1 = parts[0].strip()
    player2 = parts[1].strip()

    # Identificar si Zverev es local (player1) o visitante (player2)
    zverev_local = 'Zverev' in player1

    # Contar sets ganados
    zverev_sets = 0
    rival_sets = 0

    for set_raw in score.split():
        set_score = clean_set_score(set_raw)
        if set_score is None:
            continue
        s1, s2 = set_score
        if zverev_local:
            if s1 > s2:
                zverev_sets += 1
            elif s1 < s2:
                rival_sets += 1
        else:
            if s2 > s1:
                zverev_sets += 1
            elif s2 < s1:
                rival_sets += 1

    if zverev_sets > rival_sets:
        return 'W'
    elif rival_sets > zverev_sets:
        return 'L'
    else:
        return None  # empate o error

# Aplicar la función
df['W_or_L'] = df.apply(get_winner, axis=1)

# Guardar el nuevo archivo
df.to_csv('zverev_partidos_con_resultado2.csv', index=False)
