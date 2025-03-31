import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Generación gráficas genéticas - PyCatan")

# Parámetros del algoritmo
parser.add_argument("--extra_name", type=str, default="", help="Nombre extra para los archivos generados")
args = parser.parse_args()

extra_name = args.extra_name


# Load the CSV file
csv_filename = f"./data/{extra_name}_evolucion_fitness.csv"
df = pd.read_csv(csv_filename)

# Convert the probabilities string column into a list of floats
df["Mejor_Probabilidades"] = df["Mejor_Probabilidades"].apply(lambda x: list(map(float, x.split(","))))

# === Cargar datos de todos los individuos para calcular top 25% ===
csv_filename_all = f"./data/{extra_name}_evolucion_fitness_all.csv"
df_all = pd.read_csv(csv_filename_all)

top25_fitness = df_all.groupby("Generacion").apply(
    lambda g: g.nlargest(max(1, int(np.ceil(len(g) * 0.25))), 'Fitness')['Fitness'].mean()
).reset_index(name="Top25_Fitness")

# Calcular promedios móviles con ventana de 3 generaciones
df["Fitness_Medio_MA"] = df["Fitness_Medio"].rolling(window=3, min_periods=1).mean()
df["Fitness_Maximo_MA"] = df["Fitness_Maximo"].rolling(window=3, min_periods=1).mean()
top25_fitness["Top25_Fitness_MA"] = top25_fitness["Top25_Fitness"].rolling(window=3, min_periods=1).mean()

# Extract probability matrix
probabilities_matrix = np.array(df["Mejor_Probabilidades"].tolist()).T  # Transpose to get each probability separately

# === Plot Evolución del Fitness ===
plt.figure(figsize=(10, 5))
plt.plot(df["Generacion"], df["Fitness_Medio"], label="Fitness Medio", linestyle="--", marker="o")
plt.plot(df["Generacion"], df["Fitness_Maximo"], label="Fitness Máximo", linestyle="-", marker="s", color="red")
plt.plot(top25_fitness["Generacion"], top25_fitness["Top25_Fitness"], label="Fitness Top 25%", linestyle="-.", marker="d", color="green")

plt.plot(df["Generacion"], df["Fitness_Medio_MA"], label="MA Fitness Medio", linestyle="--", marker="o", color="blue")
plt.plot(df["Generacion"], df["Fitness_Maximo_MA"], label="MA Fitness Máximo", linestyle="-", marker="s", color="orange")
plt.plot(top25_fitness["Generacion"], top25_fitness["Top25_Fitness_MA"], label="MA Fitness Top 25%", linestyle="-.", marker="d", color="purple")

plt.xlabel("Generación")
plt.ylabel("Fitness")
plt.title("Evolución del Fitness")
plt.legend()
plt.grid()
plt.savefig(f"./data/{extra_name}_fitness_best.png")
# plt.show()

# === Plot Best Individual’s Probabilities Over Generations ===
plt.figure(figsize=(10, 6))
plt.stackplot(df["Generacion"], probabilities_matrix, labels=[f"Prob {i+1}" for i in range(probabilities_matrix.shape[0])], alpha=0.7)
plt.xlabel("Generación")
plt.ylabel("Probabilidad")
plt.title("Evolución de Probabilidades del Mejor Individuo")
plt.legend(loc="upper right", fontsize="small")
plt.grid()
plt.savefig(f"./data/{extra_name}_evolucion_prob_mejor.png")
#plt.show()


# Cargar el archivo CSV con la evolución del mejor individuo
csv_filename_best = f"./data/{extra_name}_evolucion_fitness.csv"

try:
    df_best = pd.read_csv(csv_filename_best)

    # Convertir la columna de probabilidades del mejor individuo en listas de flotantes
    df_best["Mejor_Probabilidades"] = df_best["Mejor_Probabilidades"].apply(lambda x: list(map(float, x.split(","))))

    # Expandir las probabilidades en columnas separadas (Mejor individuo)
    best_probabilities_matrix = np.array(df_best["Mejor_Probabilidades"].tolist())

    # Cargar el archivo CSV con todas las probabilidades de los individuos
    csv_filename_all = f"./data/{extra_name}_evolucion_fitness_all.csv"
    df_all = pd.read_csv(csv_filename_all)

    # Convertir la columna de probabilidades en listas de valores flotantes
    df_all["Probabilidades"] = df_all["Probabilidades"].apply(lambda x: list(map(float, x.split(","))))

    # Expandir las probabilidades en columnas separadas (Todos los individuos)
    probabilities_expanded = np.array(df_all["Probabilidades"].tolist())

    # Número de probabilidades
    num_probabilidades = probabilities_expanded.shape[1]
    offset_step = 0.05  # Pequeño desplazamiento en X

    # Crear subgráficas con colores diferentes
    fig, axes = plt.subplots(nrows=(num_probabilidades + 1) // 2, ncols=2, figsize=(14, 10))
    axes = axes.flatten()  # Aplanar la matriz de subgráficas para fácil iteración

    colors = plt.cm.viridis(np.linspace(0, 1, num_probabilidades))  # Generar colores distintos

    for i in range(num_probabilidades):  # Iterar sobre cada tipo de probabilidad
        ax = axes[i]  # Obtener el subplot correspondiente

        # Calcular posiciones con offset
        x_positions = df_all["Generacion"] + (i - num_probabilidades / 2) * offset_step
        x_positions_best = df_best["Generacion"] + (i - num_probabilidades / 2) * offset_step

        # Graficar todos los individuos con su color correspondiente
        ax.scatter(x_positions, probabilities_expanded[:, i], alpha=0.3, s=20, color=colors[i])

        # Marcar la mejor probabilidad del mejor individuo con "X" del mismo color
        ax.scatter(x_positions_best, best_probabilities_matrix[:, i],
                   marker="x", s=50, linewidths=2, color=colors[i])

        # Mostrar solo etiquetas del eje Y y título
        # ax.set_ylabel("Probabilidad", fontsize=9)
        ax.set_title(f"Prob {i+1}", fontsize=10, pad=5)
        ax.set_xticks([])  # Ocultar etiquetas del eje X

        ax.grid(True, linestyle="--", alpha=0.5)

    # Eliminar los ejes vacíos si num_probabilidades es impar
    if num_probabilidades % 2 != 0:
        fig.delaxes(axes[-1])

    # Ajustar diseño para mayor claridad
    plt.tight_layout()
    plt.savefig(f"./data/{extra_name}_fitness_all.png")
    #plt.show()

except FileNotFoundError:
    print("Uno de los archivos CSV no se encuentra en la ruta especificada.")




# # Cargar el archivo CSV con la evolución del mejor individuo
# csv_filename_best = f"./data/{extra_name}_evolucion_fitness.csv"

# try:
#     df_best = pd.read_csv(csv_filename_best)

#     # Convertir la columna de probabilidades del mejor individuo en listas de flotantes
#     df_best["Mejor_Probabilidades"] = df_best["Mejor_Probabilidades"].apply(lambda x: list(map(float, x.split(","))))

#     # Expandir las probabilidades en columnas separadas (Mejor individuo)
#     best_probabilities_matrix = np.array(df_best["Mejor_Probabilidades"].tolist())

#     # Cargar el archivo CSV con todas las probabilidades de los individuos
#     csv_filename_all = f"./data/{extra_name}_evolucion_fitness_all.csv"
#     df_all = pd.read_csv(csv_filename_all)

#     # Convertir la columna de probabilidades en listas de valores flotantes
#     df_all["Probabilidades"] = df_all["Probabilidades"].apply(lambda x: list(map(float, x.split(","))))

#     # Expandir las probabilidades en columnas separadas (Todos los individuos)
#     probabilities_expanded = np.array(df_all["Probabilidades"].tolist())

#     # Crear la figura
#     plt.figure(figsize=(12, 6))

#     # Definir el número de probabilidades y el pequeño offset
#     num_probabilidades = probabilities_expanded.shape[1]
#     offset_step = 0.05  # Pequeño desplazamiento en X

#     # Graficar todas las probabilidades de los individuos con desplazamiento en X
#     for i in range(num_probabilidades):
#         x_positions = df_all["Generacion"] + (i - num_probabilidades / 2) * offset_step  # Centrar los grupos
#         plt.scatter(x_positions, probabilities_expanded[:, i], alpha=0.2, s=20)

#     # Resaltar las probabilidades del mejor individuo con "X", pero usando el mismo color
#     for i in range(best_probabilities_matrix.shape[1]):  # Iterar sobre cada probabilidad del mejor individuo
#         x_positions_best = df_best["Generacion"] + (i - num_probabilidades / 2) * offset_step  # Mantener offset
#         plt.scatter(x_positions_best, best_probabilities_matrix[:, i],
#                     marker="x", s=50, linewidths=2)  # Misma opacidad y sin color diferente

#     plt.xlabel("Generación")
#     plt.ylabel("Probabilidad")
#     plt.title("Distribución de Probabilidades Agrupadas con Mejor Individuo Destacado")
#     plt.grid(True)
#     #plt.show()

# except FileNotFoundError:
#     print("Uno de los archivos CSV no se encuentra en la ruta especificada.")




