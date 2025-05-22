import os
from No_usar.load_data import load_all_player_data
from No_usar.compare_player import compare_players
from No_usar.generate_report import generate_text_report

def main():
    print("Cargando datos de jugadores...\n")
    player_data = load_all_player_data("Test_3/player_stats3")

    if len(player_data) < 2:
        print("Debes tener al menos dos jugadores en la carpeta 'data'.")
        return

    print("Jugadores disponibles:")
    for name in player_data:
        print("-", name)

    # Selección de jugadores
    name1 = "JannikSinner"  # input("Selecciona el primer jugador: ").strip()
    name2 = "NovakDjokovic"  # input("Selecciona el segundo jugador: ").strip()

    if name1 not in player_data or name2 not in player_data:
        print("Error: uno o ambos jugadores no existen.")
        return

    df1 = player_data[name1]
    df2 = player_data[name2]

    # Análisis comparativo
    result = compare_players(df1, df2, name1, name2)

    # Generación del informe
    report_text = generate_text_report(result["comparison"], result["recommendations"], name1, name2)

    # Crear carpeta si no existe
    os.makedirs("reports", exist_ok=True)

    # Guardar el informe
    filename = f"reports/{name1}_vs_{name2}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\nInforme generado exitosamente: {filename}")

if __name__ == "__main__":
    main()
