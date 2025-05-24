# import shutil
# shutil.copy("copia5.ipynb", "copia5_1.ipynb")



numeros= [64.4,
76.6,
75.9,
70.5,
72.2,
75.4,
63.5,
80.6,
62.3,
60.6,
67.3,
67.9,
74.7,
71.2,
69.3,
71.4,
72.1,
58.6,
65.3,
56.0,
65.6,
68.5,
82.9,
76.8,
58.1,
78.2,
83.1,
74.1,
52.1,
67.0,
64.9,
81.8,
87.7,
81.5,
76.4,
85.6,
73.6,
62.8,
72.7,
77.6,
69.9,
62.5,
72.6,
73.2,
62.9,
67.3,
79.5,
71.8,
60.8,
69.2,
75.8,
75.1,
68.9]

#calcular la media
def calcular_media(numeros):
    if not numeros:
        return 0
    return sum(numeros) / len(numeros)

print("La media es:", calcular_media(numeros))