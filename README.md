# TFG_Tennis

En este repositorio se encuentra el INFORME ANALÍTICO Y PREDICTIVO DE UN PARTIDO DE TENIS MEDIANTE IA

El link del respositorio es el siguiente: [GitHub](https://github.com/joseluis031/TFG_Tennis.git)
## Ejecución de la interfaz gráfica

### Para ver el resultado final del informe es necesario ejecutar el siguiente comando
1. py -m pip install -r requirements.txt

2. py -m streamlit run stream.py

El primer comando descargará todas las librerias necesarias para un correcto funcionamiento y el segundo comando ejecutará el script "stream.py" que abrirá la pagina web en un entorno local

Este archivo recoge todos los objetivos del proyecto accediendo a los siguientes archivos:
- agente_llm.py : para obtener el análisis del modelo de LLM
- comparativa.py: para obtener las comparativas gráficas de los jugadores enfrentados
- enfrentamientos.py: para acceder al historial de enfrentamientos
- perfiles.py: para acceder a los perfiles de cada jugador
- pred_elo: para obtener la probabilidad exacta de victoria con los rankings ELO
  
## Contenido del repositorio

### Carpeta imagenes

Contiene las imagenes de los jugadores seleccionados

### Carpeta Juego_2019_23 y Juego_2024_25

Contienen las estadísticas avanzadas para comparar ambos jugadores en el Objetivo 2

### Carpeta Limpios_llm

Contienen las estadísticas avanzadas para comparar ambos jugadores en el Objetivo 3, (más limpieza para facilitar la lectura del Prompt)

### Carpeta No usar

Contiene pruebas que se han ido realizando a lo largo del proyecto

### Carpeta OBJETIVO_1_PERFILES

Contiene las estadisticas extraidas y transformadas para poder realizar los modelos de ML del objetivo 1

### Carpeta OBJETIVO_2_COMPARATIVA

Contiene las estadisticas extraidas y transformadas para poder realizar las comaprativas del objetivo 2

### Carpeta Scrapings_DATOS

Contiene todos los archivos que se han utilizado para la extracción de datos

### Carpeta Train

Contiene todos los datos de entrenamiento utilizados para objetivo 1

### agente.ipynb

Contiene diferentes pruebas realizadas buscando optimización del prompt

### cluster_perfiles.ipynb y cluster_perfiles_clay.ipynb

Contiene diferentes algoritmos llevados a cabo para clasificar cada jugador y obtener su perfil

### dataset_3hard.csv

Contiene los partidos utilizados para el entrenamiento de los modelos

### elo_rating.csv

Contiene el ranking ELO de jugadores del top 100

### limpieza_datos_gen.ipynb

Contiene la limpieza de datos para el objetivo 1

### limpieza_total_comparativa.ipynb

Contieen la limpieza de datos para objetivo 2 y 3

### matchup_analysis.txt

Contiene diferentes pruebas que se han hecho con los prompts

### modelos1.ipynb y modelos2.ipynb

Contienen los mejores modelos realizados para la seleccion de variables del objetivo 1

### stats_Clay3_con_ELO.csv y stats_Hard3_con_ELO.csv

Contienen las variables predictorias para entrenar los modelos

### top_10_atp.csv

Contiene los perfiles de cada jugador seleccionado

