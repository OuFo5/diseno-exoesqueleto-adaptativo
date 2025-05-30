import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Cargar el CSV
file_path = "leg_vertex_data.csv"
df = pd.read_csv(file_path)

# Filtrar los vértices de interés: cadera (8), rodilla (95) y tobillo (332)
landmarks = df[df['VertexIndex'].isin([8, 95, 332])].copy()

# Reorganizar los datos en formato pivote
landmarks_pivot = landmarks.pivot(index='ObjectName', columns='VertexIndex')[['X', 'Y', 'Z']]
landmarks_pivot.columns = [f'{axis}_{vertex}' for axis, vertex in landmarks_pivot.columns]
landmarks_pivot.reset_index(inplace=True)

# Calcular las características anatómicas
landmarks_pivot['upper_leg_length'] = abs(landmarks_pivot['Y_8'] + landmarks_pivot['Y_95'])
landmarks_pivot['lower_leg_length'] = abs(landmarks_pivot['Y_95'] + landmarks_pivot['Y_332'])
landmarks_pivot['total_length'] = landmarks_pivot['upper_leg_length'] + landmarks_pivot['lower_leg_length']

# Filtrar los vértices para el cálculo del perímetro del brazo y antebrazo
upper_leg_vertices = [35, 221, 253, 254, 306, 58, 59, 61, 62, 65, 66, 68, 69, 74, 75, 290, 34]
lower_leg_vertices = [170, 232, 264, 183, 181, 180, 176, 177, 283, 281, 279, 173, 172, 301, 169]

upper_leg_data = df[df['VertexIndex'].isin(upper_leg_vertices)]
lower_leg_data = df[df['VertexIndex'].isin(lower_leg_vertices)]

# Función para calcular el perímetro sumando las distancias entre puntos consecutivos
def calculate_perimeter(data, vertices):
    perimeter = 0
    for i in range(len(vertices) - 1):
        point1 = data[data['VertexIndex'] == vertices[i]][['X', 'Y', 'Z']].values[0]
        point2 = data[data['VertexIndex'] == vertices[i + 1]][['X', 'Y', 'Z']].values[0]
        perimeter += np.linalg.norm(point1 - point2)
    return perimeter

# Calcular el perímetro para el brazo y antebrazo
upper_leg_perimeter = upper_leg_data.groupby('ObjectName').apply(lambda x: calculate_perimeter(x, upper_leg_vertices)).reset_index(name='upper_leg_width')
lower_leg_perimeter = lower_leg_data.groupby('ObjectName').apply(lambda x: calculate_perimeter(x, lower_leg_vertices)).reset_index(name='lower_leg_width')

# Unir los datos de perímetro con landmarks_pivot
landmarks_pivot = landmarks_pivot.merge(upper_leg_perimeter, on='ObjectName')
landmarks_pivot = landmarks_pivot.merge(lower_leg_perimeter, on='ObjectName')

# Aplicar clustering con KMeans para 3 tallas
k = 3
features = landmarks_pivot[['upper_leg_length', 'lower_leg_length']].copy()

kmeans = KMeans(n_clusters=k, random_state=42)
landmarks_pivot['cluster'] = kmeans.fit_predict(features)

# Asignar etiquetas de talla (S, M, L)
cluster_order = landmarks_pivot.groupby('cluster')['total_length'].mean().sort_values().index
size_labels = {cluster_order[0]: 'S', cluster_order[1]: 'M', cluster_order[2]: 'L'}
landmarks_pivot['size'] = landmarks_pivot['cluster'].map(size_labels)
print(landmarks_pivot[['ObjectName', 'upper_leg_length', 'lower_leg_length', 'total_length', 'cluster', 'size']])

# Generar las gráficas
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Colores para los clusters
colors = ['blue', 'green', 'red']
size_labels = {cluster_order[0]: 'S', cluster_order[1]: 'M', cluster_order[2]: 'L'}
color_map = {cluster: color for cluster, color in zip(cluster_order, colors)}

# Gráfico 1: Ancho del Muslo vs. Longitud Total de la Pierna
for cluster, color in color_map.items():
    subset = landmarks_pivot[landmarks_pivot['cluster'] == cluster]
    axes[0].scatter(subset['total_length'], subset['upper_leg_width'], 
                    c=color, label=size_labels[cluster], s=50)
axes[0].set_xlabel('Longitud Total de la Pierna (m)')
axes[0].set_ylabel('Ancho de la zona proximal (m)')
axes[0].legend(title='Talla', loc='lower right')

# Gráfico 2: Ancho de la Tibia vs. Longitud Total de la Pierna
for cluster, color in color_map.items():
    subset = landmarks_pivot[landmarks_pivot['cluster'] == cluster]
    axes[1].scatter(subset['total_length'], subset['lower_leg_width'], 
                    c=color, label=size_labels[cluster], s=50)
axes[1].set_xlabel('Longitud Total de la Pierna (m)')
axes[1].set_ylabel('Ancho de la zona distal (m)')
axes[1].legend(title='Talla', loc='lower right')

# Ajustar diseño
plt.tight_layout()
plt.show()

# GUARDAR LOS RESULTADOS
# Fusionar con los datos de clusters y tallas usando 'ObjectName' como clave
merged_data = df.merge(
    landmarks_pivot[['ObjectName', 'total_length', 'upper_leg_width', 'lower_leg_width', 'cluster', 'size']], 
    on='ObjectName', 
    how='left'
)

# Guardar el resultado en un nuevo archivo CSV
output_path = "leg_vertex_data_with_sizes.csv"
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
output_path = "leg_vertex_stats_by_size.csv"
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
ax.set_ylabel('Longitud Total del la Pierna (m)')
ax.set_title('Rangos de Longitudes Totales de la Pierna por Talla')

# Añadir etiquetas de los valores mínimos y máximos
for i, row in size_ranges.iterrows():
    ax.text(row['size'], row['min'], f"{row['min']:.2f}", ha='center', va='bottom')
    ax.text(row['size'], row['max'], f"{row['max']:.2f}", ha='center', va='top')

plt.show()

# Visualizar cantidad y porcentaje de modelos por cluster/talla
count_by_size = landmarks_pivot['size'].value_counts().reset_index()
count_by_size.columns = ['size', 'count']
count_by_size['percentage'] = 100 * count_by_size['count'] / count_by_size['count'].sum()
print(count_by_size)