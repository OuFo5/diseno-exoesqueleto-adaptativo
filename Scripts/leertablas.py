import pandas as ps
import numpy as np

# Cargar el CSV
file_path = "models/arm/model_metadata.csv"
df = ps.read_csv(file_path)
print(df)