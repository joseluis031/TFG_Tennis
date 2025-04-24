
from load_data import load_all_player_data

def main():
    print("Cargando datos de jugadores...")
    player_data = load_all_player_data("Test_3/player_stats3")

    print("Jugadores disponibles:")
    for name in player_data:
        print("-", name)

    # Aquí irá más lógica para seleccionar jugadores y generar informes

if __name__ == "__main__":
    main()
