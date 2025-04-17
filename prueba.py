import pandas as pd
import os

# Carpetas
input_folder = 'Tests/calidad_de_resto'
output_folder = 'Tests/calidad_de_resto_limpio'
os.makedirs(output_folder, exist_ok=True)

# Procesar cada CSV en la carpeta
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        input_path = os.path.join(input_folder, filename)
        df = pd.read_csv(input_path)

        if 'Result' not in df.columns:
            print(f"{filename}: no se encontró columna 'Result', se omite.")
            continue

        # Limpiar columna Result y dividirla
        df['Result'] = df['Result'].astype(str).str.strip()
        df['W_or_L'] = df['Result'].str[0]
        df['Rival'] = df['Result'].str.extract(r'vs(.+)', expand=False).str.strip()

        # Eliminar columna original
        df = df.drop(columns=['Result'])

        # Guardar nuevo CSV
        output_path = os.path.join(output_folder, filename)
        df.to_csv(output_path, index=False)
        print(f"{filename} procesado correctamente.")
