import bpy
import csv
import os

# Configuration parameters
# If you want to extract all vertices, leave vertex_indices as None.
# If you only want to extract specific indices (e.g., the elbow vertex), specify the list.
vertex_indices = None  

# Define the output path for the CSV file (saved in the same folder as the .blend file)
output_filepath = os.path.join(bpy.path.abspath("//"), "leftarm_vertex_data.csv")

# Open (or create) the CSV file in write mode.
with open(output_filepath, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write the CSV header.
    writer.writerow(["ObjectName", "VertexIndex", "X", "Y", "Z"])
    
    # Iterate over all objects in the scene
    for obj in bpy.data.objects:
        # Process only mesh objects
        if obj.type == 'MESH':
            mesh = obj.data
            
            if vertex_indices is None:
                # Extract all vertices from the object
                for vertex in mesh.vertices:
                    co = vertex.co  # local coordinates
                    writer.writerow([obj.name, vertex.index, co.x, co.y, co.z])
            else:
                # Extract only the vertices specified in vertex_indices
                for index in vertex_indices:
                    if index < len(mesh.vertices):
                        vertex = mesh.vertices[index]
                        co = vertex.co
                        writer.writerow([obj.name, vertex.index, co.x, co.y, co.z])
                    else:
                        print(f"Object {obj.name} does not have a vertex with index {index}")

print("Export completed. File saved at:", output_filepath)
