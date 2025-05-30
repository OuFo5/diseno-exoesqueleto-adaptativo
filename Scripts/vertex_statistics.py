import pandas as pd
import numpy as np
import os

def analyze_vertex_data(csv_path):
    """
    Load the CSV file, perform statistical analysis, and generate key visualizations.
    """
    # Verificar si el archivo existe
    if not os.path.exists(csv_path):
        print(f"Error: El archivo {csv_path} no existe.")
        return

    # Cargar el CSV
    df = pd.read_csv(csv_path)

    # Verificar que las columnas necesarias existen
    required_columns = {"VertexIndex", "X", "Y", "Z"}
    if not required_columns.issubset(df.columns):
        print(f"Error: El CSV debe contener las columnas {required_columns}, pero tiene {df.columns}.")
        return

    # Convertir las columnas a valores numéricos
    df[["X", "Y", "Z"]] = df[["X", "Y", "Z"]].apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)

    # Calcular estadísticas para cada coordenada
    stats_summary = df.groupby("VertexIndex")[["X", "Y", "Z"]].describe()

    # Calcular la desviación estándar combinada para cada vértice
    stats_summary["Std_Combined"] = np.sqrt(
        stats_summary[("X", "std")]**2 + stats_summary[("Y", "std")]**2 + stats_summary[("Z", "std")]**2
    )

    # Guardar estadísticas en CSV
    output_csv = "leftarm_vertex_statistics.csv"
    stats_summary.to_csv(output_csv)
    
    print("\nDataset Overview:")
    print(df.head())
    print("\nStatistical Summary:")
    print(stats_summary)
    print(f"\nStatistical summary saved to {output_csv}")

# Llamar a la función
csv_path = "leftarm_vertex_data.csv"
analyze_vertex_data(csv_path)