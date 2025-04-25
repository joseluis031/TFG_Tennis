from openai import OpenAI

def generate_text_report_gpt(comparison, recommendations, name1, name2, api_key, model="gpt-3.5-turbo"):
    client = OpenAI(api_key=api_key)

    prompt_intro = (
        f"Actúa como un analista deportivo profesional especializado en tenis.\n"
        f"Compara a los jugadores {name1} y {name2} usando los datos proporcionados.\n"
        f"Redacta un informe completo en lenguaje natural con estilo técnico, incluyendo:\n"
        f"- Fortalezas y debilidades estadísticas de cada jugador.\n"
        f"- Comparación directa entre ambos.\n"
        f"- Recomendaciones estratégicas personalizadas para que cada uno derrote al otro.\n"
        f"- Justifica cada recomendación usando datos específicos.\n"
    )

    player1_stats = f"\nEstadísticas de {name1}:\n{comparison[name1]}"
    player2_stats = f"\nEstadísticas de {name2}:\n{comparison[name2]}"
    recs_text = f"\nRecomendaciones automáticas:\n{recommendations}"

    full_prompt = prompt_intro + player1_stats + player2_stats + recs_text

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un analista deportivo experto en tenis profesional."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error al generar informe con GPT: {e}"
