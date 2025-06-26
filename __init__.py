# __init__.py

# Import the class from your nodes.py file
from .nodes import SaveImageEXR_Deployable

# A dictionary that maps the internal name of the node to the node class
NODE_CLASS_MAPPINGS = {
    "SaveImageEXR_Deployable": SaveImageEXR_Deployable
}

# A dictionary that maps the internal name to the name displayed in the ComfyUI menu
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageEXR_Deployable": "Save EXR (Deployable)"
}

print("✅ Loaded Custom Node: ComfyDeploy_EXR_Saver")