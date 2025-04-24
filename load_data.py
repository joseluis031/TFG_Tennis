import os
import pandas as pd

def load_all_player_data(data_dir):
    player_data = {}
    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            player_name = filename.replace("_matches_full_con_WorL.csv", "")
            path = os.path.join(data_dir, filename)
            df = pd.read_csv(path)
            player_data[player_name] = df
    return player_data
