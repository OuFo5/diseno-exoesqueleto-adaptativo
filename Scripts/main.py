import sys
import os
import bpy


# Directory configuration
script_dir = r"C:\Users\oscar\OneDrive - Universidad de los andes\Universidad\TESIS\Proyecto"
sys.path.append(script_dir)

from models_generator import generate_smplx_model, generate_metadata

# Generate Models
num_models = 200 #Number of models to generate for each gender
metadata_dict = {"index": [], "gender": []} # Metadata dict
for index in range(num_models):
    generate_smplx_model("male", index, metadata_dict)
    generate_smplx_model("female", index, metadata_dict)
    
# Guardar los metadatos
generate_metadata(metadata_dict)
