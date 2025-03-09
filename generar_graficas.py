import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
csv_filename = "./data/evolucion_fitness.csv"
df = pd.read_csv(csv_filename)

# Convert the probabilities string column into a list of floats
df["Mejor_Probabilidades"] = df["Mejor_Probabilidades"].apply(lambda x: list(map(float, x.split(","))))

# Extract probability matrix
probabilities_matrix = np.array(df["Mejor_Probabilidades"].tolist()).T  # Transpose to get each probability separately

# === Plot Fitness Evolution ===
plt.figure(figsize=(10, 5))
plt.plot(df["Generacion"], df["Fitness_Medio"], label="Fitness Medio", linestyle="--", marker="o")
plt.plot(df["Generacion"], df["Fitness_Maximo"], label="Fitness Máximo", linestyle="-", marker="s", color="red")
plt.xlabel("Generación")
plt.ylabel("Fitness")
plt.title("Evolución del Fitness")
plt.legend()
plt.grid()
plt.show()

# === Plot Best Individual’s Probabilities Over Generations ===
plt.figure(figsize=(10, 6))
plt.stackplot(df["Generacion"], probabilities_matrix, labels=[f"Prob {i+1}" for i in range(probabilities_matrix.shape[0])], alpha=0.7)
plt.xlabel("Generación")
plt.ylabel("Probabilidad")
plt.title("Evolución de Probabilidades del Mejor Individuo")
plt.legend(loc="upper right", fontsize="small")
plt.grid()
plt.show()
