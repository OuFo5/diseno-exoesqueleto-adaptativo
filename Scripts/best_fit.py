import bpy
import csv
import os

# Ruta al archivo CSV
csv_path = r"C:\Users\oscar\OneDrive - Universidad de los andes\Universidad\TESIS\Proyecto\leg_vertex_statistics.csv"


# Función para importar datos de los vértices y su desviación estándar
def import_vertices_from_csv(csv_path):
    vertices = []
    std_devs = []

    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                x = float(row['X'])
                y = float(row['Y'])
                z = float(row['Z'])
                std_dev = float(row['Std_Combined'])  # Extraer desviación estándar

                vertices.append((x, y, z))
                std_devs.append(std_dev)
            except ValueError:
                continue  # Omitir filas con errores

    print(f"Loaded {len(vertices)} vertices from CSV.")
    
    return vertices, std_devs

# Función para escalar los valores de desviación estándar a [0,1]
def scale_weights(std_devs):

    # Obtener valores mínimo y máximo
    min_std = 0.000
    max_std = 0.024
    print(f"MIN_Std = {min_std}", f"MAX_Std = {max_std}")

    if max_std == min_std:  # Evitar división por cero
        return [0.5] * len(std_devs)

    weights = [(std - min_std) / (max_std - min_std) for std in std_devs]  # Normalización

    return weights

# Actualizar la malla con los nuevos vértices
def update_mesh_vertices(mesh_name, vertices):
    obj = bpy.data.objects.get(mesh_name)
    if obj and obj.type == 'MESH':
        mesh = obj.data
        for i, vert in enumerate(mesh.vertices):
            if i < len(vertices):
                vert.co = vertices[i]
        mesh.update()
        print(f"Updated {len(vertices)} vertices in {mesh_name}.")
    else:
        print(f"Mesh '{mesh_name}' not found.")

# Aplicar "Weight Painting" basado en los valores escalados
def apply_weight_paint(mesh_name, weights):
    obj = bpy.data.objects.get(mesh_name)
    if obj and obj.type == 'MESH':
        if not obj.vertex_groups:
            obj.vertex_groups.new(name="Std_Deviation_Weights")
        
        vgroup = obj.vertex_groups.active

        for i, weight in enumerate(weights):
            vgroup.add([i], weight, 'REPLACE')

        print("\nFinal Weights Applied")
        for i in range(min(592, len(weights))):
            print(f"Vertex {i}: Std_Dev = {std_devs[i]:.6f}, Weight = {weights[i]:.6f}")

        print(f"Applied weight painting to {len(weights)} vertices.")
    else:
        print(f"Mesh '{mesh_name}' not found.")

# Ejecutar todo
mesh_name = "SMPLX-mesh"
vertices, std_devs = import_vertices_from_csv(csv_path)
weights = scale_weights(std_devs)  # Escalar con factor
update_mesh_vertices(mesh_name, vertices)
apply_weight_paint(mesh_name, weights)



