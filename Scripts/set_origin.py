import bpy

def set_origin_to_vertex(obj, vertex_index):
    # Ensure the object is selected and active
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Verify that the vertex index is valid
    if vertex_index >= len(obj.data.vertices):
        print(f"Index {vertex_index} out of range in {obj.name}")
        return

    # Get the global location of the vertex
    vertex = obj.data.vertices[vertex_index].co
    vertex_global = obj.matrix_world @ vertex

    # Set the origin to the specified vertex
    bpy.context.scene.cursor.location = vertex_global
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    # Move the object to the global origin (0,0,0)
    obj.location = (0, 0, 0)

    print(f"{obj.name} aligned successfully.")

def align_all_objects(vertex_index=0):
    # Filter only MESH objects
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    print(f"Processing {len(mesh_objects)} objects...")

    for obj in mesh_objects:
        set_origin_to_vertex(obj, vertex_index)

# Select Vertex
i_vertex = 128 # align respect knee
#i_vertex = 268 # align respect elbow
align_all_objects(vertex_index=i_vertex)
