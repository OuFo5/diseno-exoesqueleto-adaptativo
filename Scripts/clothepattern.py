import bpy
import bmesh
import numpy as np
import os

# Obtener el objeto activo
obj = bpy.context.object
if obj is None or obj.type != 'MESH':
    raise ValueError("Selecciona un objeto tipo MESH.")

# Crear un BMesh para manipular la geometría
bm = bmesh.new()
bm.from_mesh(obj.data)

# Obtener vértices y caras
verts = np.array([v.co[:] for v in bm.verts])
faces = [[v.index for v in f.verts] for f in bm.faces]

# Desplegar la malla en 2D respetando las costuras (usando UV Unwrap)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')

# Obtener coordenadas UV
uv_layer = bm.loops.layers.uv.active
if uv_layer is None:
    raise ValueError("No se generaron coordenadas UV. Asegúrate de que la malla tiene costuras.")

uv_coords = []
for face in bm.faces:
    for loop in face.loops:
        uv_coords.append(loop[uv_layer].uv[:])

uv_coords = np.array(uv_coords)

# Normalizar UV para exportación
min_vals = uv_coords.min(axis=0)
max_vals = uv_coords.max(axis=0)
uv_coords = (uv_coords - min_vals) / (max_vals - min_vals)  # Normaliza

# Guardar como archivo SVG para impresión
output_path = bpy.path.abspath("C:/Users/oscar/OneDrive - Universidad de los andes/Universidad/TESIS/Proyecto/Diseño EXO/manga_pattern.svg")
with open(output_path, "w") as f:
    f.write("<svg width='1000' height='1000' xmlns='http://www.w3.org/2000/svg'>\n")
    scale = 800  # Escalado para mejor visualización en SVG
    offset = 100  # Margen en SVG
    
    for face in faces:
        points = " ".join(f"{uv_coords[v][0]*scale+offset},{uv_coords[v][1]*scale+offset}" for v in face)
        f.write(f"<polygon points='{points}' style='fill:none;stroke:black;stroke-width:1'/>\n")
    
    f.write("</svg>")

bm.free()
print(f"Patrón guardado en: {output_path}")
