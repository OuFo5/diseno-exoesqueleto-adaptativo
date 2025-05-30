import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Cargar el CSV
file_path = "leftarm_vertex_data.csv"
df = pd.read_csv(file_path)

# Filtrar los vértices de interés: hombro (367), codo (264) y muñeca (530)
landmarks = df[df['VertexIndex'].isin([367, 264, 530])].copy()

# Reorganizar los datos en formato pivote
landmarks_pivot = landmarks.pivot(index='ObjectName', columns='VertexIndex')[['X', 'Y', 'Z']]
landmarks_pivot.columns = [f'{axis}_{vertex}' for axis, vertex in landmarks_pivot.columns]
landmarks_pivot.reset_index(inplace=True)

# Calcular las características anatómicas
landmarks_pivot['upper_arm_length'] = abs(landmarks_pivot['X_367'] - landmarks_pivot['X_264'])
landmarks_pivot['forearm_length'] = abs(landmarks_pivot['X_264'] - landmarks_pivot['X_530'])
landmarks_pivot['total_length'] = landmarks_pivot['upper_arm_length'] + landmarks_pivot['forearm_length']

# Filtrar los vértices para el cálculo del perímetro del brazo y antebrazo
upper_arm_vertices = [4, 5, 46, 73, 75, 86, 87, 101, 102, 98, 99, 56, 57, 95, 92, 91, 106, 107]
forearm_vertices = [208, 294, 295, 330, 170, 169, 335, 161, 162, 188, 187, 300, 159, 155, 156, 209]

upper_arm_data = df[df['VertexIndex'].isin(upper_arm_vertices)]
forearm_data = df[df['VertexIndex'].isin(forearm_vertices)]

# Función para calcular el perímetro sumando las distancias entre puntos consecutivos
def calculate_perimeter(data, vertices):
    perimeter = 0
    for i in range(len(vertices) - 1):
        point1 = data[data['VertexIndex'] == vertices[i]][['X', 'Y', 'Z']].values[0]
        point2 = data[data['VertexIndex'] == vertices[i + 1]][['X', 'Y', 'Z']].values[0]
        perimeter += np.linalg.norm(point1 - point2)
    return perimeter

# Calcular el perímetro para el brazo y antebrazo
upper_arm_perimeter = upper_arm_data.groupby('ObjectName').apply(lambda x: calculate_perimeter(x, upper_arm_vertices)).reset_index(name='upper_arm_width')
forearm_perimeter = forearm_data.groupby('ObjectName').apply(lambda x: calculate_perimeter(x, forearm_vertices)).reset_index(name='forearm_width')

# Unir los datos de perímetro con landmarks_pivot
landmarks_pivot = landmarks_pivot.merge(upper_arm_perimeter, on='ObjectName')
landmarks_pivot = landmarks_pivot.merge(forearm_perimeter, on='ObjectName')

# Aplicar clustering con KMeans para 3 tallas
k = 3
features = landmarks_pivot[['upper_arm_length', 'forearm_length']].copy()

kmeans = KMeans(n_clusters=k, random_state=42)
landmarks_pivot['cluster'] = kmeans.fit_predict(features)

# Asignar etiquetas de talla (S, M, L)
cluster_order = landmarks_pivot.groupby('cluster')['total_length'].mean().sort_values().index
size_labels = {cluster_order[0]: 'S', cluster_order[1]: 'M', cluster_order[2]: 'L'}
landmarks_pivot['size'] = landmarks_pivot['cluster'].map(size_labels)
print(landmarks_pivot[['ObjectName', 'upper_arm_length', 'forearm_length', 'total_length', 'cluster', 'size']])

# Generar las gráficas
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Colores para los clusters
colors = ['blue', 'green', 'red']
size_labels = {cluster_order[0]: 'S', cluster_order[1]: 'M', cluster_order[2]: 'L'}
color_map = {cluster: color for cluster, color in zip(cluster_order, colors)}

# Gráfico 1: Ancho del brazo vs. Longitud total del brazo
for cluster, color in color_map.items():
    subset = landmarks_pivot[landmarks_pivot['cluster'] == cluster]
    axes[0].scatter(subset['total_length'], subset['upper_arm_width'], 
                    c=color, label=size_labels[cluster], s=50)
axes[0].set_xlabel('Longitud Total del Brazo (m)')
axes[0].set_ylabel('Ancho de la zona proximal (m)')
axes[0].legend(title='Talla', loc='lower right')

# Gráfico 2: Ancho del antebrazo vs. Longitud total del brazo
for cluster, color in color_map.items():
    subset = landmarks_pivot[landmarks_pivot['cluster'] == cluster]
    axes[1].scatter(subset['total_length'], subset['forearm_width'], 
                    c=color, label=size_labels[cluster], s=50)
axes[1].set_xlabel('Longitud Total del Brazo (m)')
axes[1].set_ylabel('Ancho de la zona distal (m)')
axes[1].legend(title='Talla', loc='lower right')

# Ajustar diseño
plt.tight_layout()
plt.show()

# GUARDAR LOS RESULTADOS
# Fusionar con los datos de clusters y tallas usando 'ObjectName' como clave
merged_data = df.merge(
    landmarks_pivot[['ObjectName', 'total_length', 'upper_arm_width', 'forearm_width', 'cluster', 'size']], 
    on='ObjectName', 
    how='left'
)

# Guardar el resultado en un nuevo archivo CSV
output_path = "leftarm_vertex_data_with_sizes.csv"
merged_data.to_csv(output_path, index=False)

# Mostrar algunas filas del archivo resultante
merged_data.head()

# ESTADÍSTICAS POR VÉRTICE Y POR TALLA
# Calcular estadísticas por vértice y por talla
stats_by_size = merged_data.groupby(['size', 'VertexIndex'])[['X', 'Y', 'Z']].agg(['mean', 'std', 'min', 'max']).reset_index()

# Calcular la desviación estándar combinada para cada vértice y talla
stats_by_size['Std_Combined'] = np.sqrt(
    stats_by_size[('X', 'std')]**2 + stats_by_size[('Y', 'std')]**2 + stats_by_size[('Z', 'std')]**2
)

# Renombrar columnas para mayor claridad
stats_by_size.columns = ['_'.join(col).strip('_') for col in stats_by_size.columns.values]

# Guardar los resultados en un nuevo CSV
output_path = "leftarm_vertex_stats_by_size.csv"
stats_by_size.to_csv(output_path, index=False)

# Mostrar algunas filas de la tabla resultante
stats_by_size.head()

# Calcular los rangos de longitudes para cada talla
size_ranges = landmarks_pivot.groupby('size')['total_length'].agg(['min', 'max']).reset_index()

# Imprimir los rangos
print(size_ranges)

# Visualizar los rangos de longitudes para cada talla
fig, ax = plt.subplots(figsize=(10, 6))

# Crear un gráfico de barras para los rangos de longitudes
ax.bar(size_ranges['size'], size_ranges['max'] - size_ranges['min'], bottom=size_ranges['min'], color=['blue', 'green', 'red'])

# Añadir etiquetas y título
ax.set_xlabel('Talla')
ax.set_ylabel('Longitud Total del Brazo (m)')
ax.set_title('Rangos de Longitudes Totales del Brazo por Talla')

# Añadir etiquetas de los valores mínimos y máximos
for i, row in size_ranges.iterrows():
    ax.text(row['size'], row['min'], f"{row['min']:.2f}", ha='center', va='bottom')
    ax.text(row['size'], row['max'], f"{row['max']:.2f}", ha='center', va='top')

plt.show()

# Visualizar cantidad y porcentaje de modelos por cluster/talla
count_by_size = landmarks_pivot['size'].value_counts().reset_index()
count_by_size.columns = ['size', 'count']
count_by_size['percentage'] = 100 * count_by_size['count'] / count_by_size['count'].sum()

# Calcular outliers por talla usando el método IQR
outlier_counts = []
outlier_percentages = []
for size in count_by_size['size']:
    group = landmarks_pivot[landmarks_pivot['size'] == size]
    q1 = group['total_length'].quantile(0.25)
    q3 = group['total_length'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = group[(group['total_length'] < lower_bound) | (group['total_length'] > upper_bound)]
    outlier_counts.append(len(outliers))
    if len(group) > 0:
        outlier_percentages.append(100 * len(outliers) / len(group))
    else:
        outlier_percentages.append(0)
count_by_size['outlier_count'] = outlier_counts
count_by_size['outlier_percentage'] = outlier_percentages

print(count_by_size)