import os
from load_data import load_all_player_data
from compare_player import compare_players
from generate_report_gpt import generate_text_report_gpt

def main():
    print("Cargando datos de jugadores...\n")
    player_data = load_all_player_data("Test_3/player_stats3")

    if len(player_data) < 2:
        print("Debes tener al menos dos jugadores en la carpeta 'Test_3/player_stats3'.")
        return

    print("Jugadores disponibles:")
    for name in player_data:
        print("-", name)

    # Selección de jugadores
    name1 = "JannikSinner"  # input("Selecciona el primer jugador: ").strip()
    name2 = "DaniilMedvedev"

    if name1 not in player_data or name2 not in player_data:
        print("Error: uno o ambos jugadores no existen.")
        return

    # Solicitar API key
    api_key = "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"
    if not api_key:
        print("API Key no proporcionada.")
        return

    df1 = player_data[name1]
    df2 = player_data[name2]

    # Comparación y recomendaciones
    result = compare_players(df1, df2, name1, name2)
    comparison = result["comparison"]
    recommendations = result["recommendations"]

    # Redactar informe con GPT
    print("\nGenerando informe con GPT (puede tardar unos segundos)...")
    report_text = generate_text_report_gpt(comparison, recommendations, name1, name2, api_key)

    # Guardar el informe
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{name1}_vs_{name2}_GPT.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\nInforme generado exitosamente: {filename}")

if __name__ == "__main__":
    main()
