import bpy
import os
import sys
import csv
import numpy as np

# Directory configuration
script_dir = r"C:\Users\oscar\OneDrive - Universidad de los andes\Universidad\TESIS\Proyecto"
sys.path.append(script_dir)

from functions import load_csv, create_vertex_group, split_part, delete_object, export_model, get_model_metadata

# Output directory
output_directory = r"C:\Users\oscar\OneDrive - Universidad de los andes\Universidad\TESIS\Proyecto\models\leg"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
# Input directory
csv_file = os.path.join(script_dir, "vertex_groups.csv")
vertex_groups = load_csv(csv_file)


def generate_smplx_model(gender, index, metadata_dict):
    """
    Generates a random SMPL-X model with the specified gender, separates specific body parts,
    and removes unnecessary objects (original mesh and armature).

    :param gender (str): Gender of the model. Accepted values: "male", "female".
    :param index (int): Model index number for identification.
    """
    print(f"Generating {gender} model {index}...")

    # Clean the scene by removing all existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Set the SMPL-X model
    bpy.data.window_managers["WinMan"].smplx_tool.smplx_gender = gender
    bpy.ops.scene.smplx_add_gender()
    smplx_model = bpy.context.object

    if smplx_model:
        bpy.ops.object.smplx_random_shape()
        bpy.ops.object.smplx_update_joint_locations()

        smplx_model.location = (0, 0, 0)
        smplx_model.rotation_euler = (0, 0, 0)

        mesh_name = f"SMPLX-mesh-{gender}"
        # Get betas
        betas = []
        obj = bpy.data.objects[mesh_name]
        for key_block in obj.data.shape_keys.key_blocks:
            if key_block.name.startswith("Shape"):
                betas.append(key_block.value)
        
        metadata_dict["index"].append(index)
        metadata_dict["gender"].append(gender)
        
        num_betas = len(betas)
        for i in range(num_betas):
            beta_key = f"beta_{i}"
            if beta_key not in metadata_dict:
                metadata_dict[beta_key] = []
            metadata_dict[beta_key].append(betas[i])

        for group_name, vertices in vertex_groups.items():
            create_vertex_group(mesh_name, group_name, vertices)

        groups = ["left_thigh", "left_leg"]
        separated_parts = split_part(mesh_name, groups)

        bpy.ops.object.select_all(action='DESELECT')
        if mesh_name in bpy.data.objects:
            bpy.context.view_layer.objects.active = smplx_model
            smplx_model.select_set(True)
            bpy.ops.object.delete()
            print(f"Original object '{mesh_name}' eliminado.")
        
        bpy.ops.object.select_by_type(type="ARMATURE")
        bpy.ops.object.delete()
        
        export_path = os.path.join(output_directory, f"{gender}_model_{index}.obj")
        export_model(export_path)
        print(f"Exported: {export_path}")
        
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
    else:
        print("Error: Model generation failed!")

def generate_metadata(metadata_dict):
    """
    Guarda el diccionario de metadatos en un archivo CSV.

    :param metadata_dict: (dict) Diccionario con metadatos de los modelos
    """
    filepath = os.path.join(output_directory, "model_metadata.csv")
    with open(filepath, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=metadata_dict.keys())
        writer.writeheader()

        # Escribir cada fila del CSV
        for i in range(len(metadata_dict["index"])):
            row = {key: metadata_dict[key][i] for key in metadata_dict}
            writer.writerow(row)
    print(f"Metadata saved at {filepath}")

    