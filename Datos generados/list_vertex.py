import bpy

# Get the active object
obj = bpy.context.object

if obj and obj.type == 'MESH':
    # Ensure we are in OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get the selected vertices' indices
    selected_verts = [v.index for v in obj.data.vertices if v.select]

    # Print and store the vertex indices
    print("Selected Vertex Indices:", selected_verts)

    # Save the list (you can copy it manually after running)
    stored_vertex_list = selected_verts

    # Switch back to Edit Mode (optional)
    bpy.ops.object.mode_set(mode='EDIT')
else:
    print("Active object is not a mesh.")
