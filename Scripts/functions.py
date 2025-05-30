import bpy
import csv
import random
import bmesh
import numpy as np


def load_csv(file_path):
    """
    Reads a CSV file and converts it back into a dictionary of vertex groups.
    
    :param file_path: Path to the CSV file.
    :return: Dictionary where keys are group names and values are lists of vertex indices.
    """
    vertex_groups = {}

    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read column names (group names)

        # Initialize empty lists for each group
        for group in headers:
            vertex_groups[group] = []

        # Read each row and append values to the correct group
        for row in reader:
            for i, value in enumerate(row):
                if value.isdigit():  # Ensure the value is a number
                    vertex_groups[headers[i]].append(int(value))

    return vertex_groups


def create_vertex_group(mesh_name, group_name, vertex_list):
    """
    Creates a vertex group in a given object.

    :param mesh_name: Name of the object in the scene.
    :param group_name: Name of the vertex group to create.
    :param vertex_list: List of vertex indices to add to the group.
    """
    # Get the object
    obj = bpy.data.objects.get(mesh_name)

    if obj and obj.type == 'MESH':
        # Ensure we are in OBJECT mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='OBJECT')

        # Create the vertex group
        group = obj.vertex_groups.new(name=group_name)

        # Add the vertices to the group
        if vertex_list:
            group.add(vertex_list, 1.0, 'ADD')
            print(f"Vertex group '{mesh_name}' created in '{mesh_name}' with {len(vertex_list)} vertices.")
        else:
            print("The vertex list is empty.")

        # Switch back to Edit Mode (optional)
        bpy.ops.object.mode_set(mode='EDIT')
    else:
        print(f"Object '{mesh_name}' not found or is not a mesh.")
        

def split_part(obj_name, group_names):
    """
    Clones and separates vertices from specified vertex groups in a given object.

    :param obj_name: Name of the object in the scene.
    :param group_names: List of vertex group names to clone and separate.
    """
    # Get the object by its name
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        print(f"Object '{obj_name}' not found.")
        return

    # Ensure we are in object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Make sure the object is selected and active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Deselect all vertices
    bpy.ops.mesh.select_all(action='DESELECT')

    # Switch back to object mode to manipulate vertex selection
    bpy.ops.object.mode_set(mode='OBJECT')

    # Select vertices belonging to the specified vertex groups
    for group_name in group_names:
        if group_name in obj.vertex_groups:
            group_index = obj.vertex_groups[group_name].index

            for v in obj.data.vertices:
                for g in v.groups:
                    if g.group == group_index:
                        v.select = True
        else:
            print(f"Vertex group '{group_name}' not found in object '{obj_name}'.")

    # Return to edit mode to perform mesh operations
    bpy.ops.object.mode_set(mode='EDIT')

    # Duplicate and separate the selected vertices
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='SELECTED')

    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    print(f"Vertex groups {group_names} have been cloned.")


def delete_object(obj):
    if obj and obj.name in bpy.data.objects:
        bpy.data.objects.remove(obj)
        print(f"Deleted: {obj_name}")
        
        
def export_model(filepath):
    bpy.ops.wm.obj_export(filepath=filepath)
        

def get_model_metadata():
    wm = bpy.data.window_managers["WinMan"].smplx_tool
    height = wm.smplx_height  # Ajusta según el nombre exacto de la propiedad
    weight = wm.smplx_weight  # Ajusta según el nombre exacto de la propiedad
    return height, weight
