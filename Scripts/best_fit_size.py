import bpy
import csv
import os
import numpy as np

# Ruta al archivo CSV
csv_path = r"C:\Users\oscar\OneDrive - Universidad de los andes\Universidad\TESIS\Proyecto\leg_vertex_stats_by_size.csv"

# Función para importar datos de los vértices y su desviación estándar

def import_vertices_by_size(csv_path):
    data_by_size = {}
    
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                size = row['size']
                vertex_index = int(row['VertexIndex'])
                x = float(row['X_mean'])
                y = float(row['Y_mean'])
                z = float(row['Z_mean'])
                std_combined = float(row['Std_Combined'])
                
                if size not in data_by_size:
                    data_by_size[size] = {'vertices': {}, 'std_devs': {}}
                
                data_by_size[size]['vertices'][vertex_index] = (x, y, z)
                data_by_size[size]['std_devs'][vertex_index] = std_combined
            except ValueError:
                continue
    
    print(f"Loaded data for {len(data_by_size)} sizes from CSV.")
    return data_by_size

# Función para escalar los valores de desviación estándar a [0,1]
def scale_weights(std_devs):
    min_std = 0.00
    max_std = 0.024
    print(f"MIN_Std={min_std}, MAX_Std={max_std}")
    
    if max_std == min_std:
        return {i: 0.5 for i in std_devs}
    
    return {i: (std - min_std) / (max_std - min_std) for i, std in std_devs.items()}

# Actualizar la malla existente en Blender
def update_mesh_vertices(mesh_name, vertices):
    obj = bpy.data.objects.get(mesh_name)
    if obj and obj.type == 'MESH':
        mesh = obj.data
        for i, vert in enumerate(mesh.vertices):
            if i in vertices:
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
        
        for i, weight in weights.items():
            vgroup.add([i], weight, 'REPLACE')
        
        print("\nFinal Weights Applied")
        for i in range(min(592, len(weights))): 
            print(f"Vertex {i}: Std_Dev = {std_devs[i]:.6f}, Weight = {weights[i]:.6f}")
        
        print(f"Applied weight painting to {len(weights)} vertices in {mesh_name}.")
    else:
        print(f"Mesh '{mesh_name}' not found.")

# Ejecutar el proceso
data_by_size = import_vertices_by_size(csv_path)
for size, data in data_by_size.items():
    mesh_name = f"SMPLX-mesh-{size}"
    update_mesh_vertices(mesh_name, data['vertices'])
    weights = scale_weights(data['std_devs'])
    apply_weight_paint(mesh_name, weights)

print("All meshes updated and weight painting applied.")
