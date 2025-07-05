# nodes.py

import os
import re
import numpy as np
import folder_paths

# Try to set up OpenCV for EXR writing. This is more reliable for deployment.
try:
    os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    print("Warning: OpenCV not found. EXR saving may fail. Please add opencv-python-headless to requirements.txt")
    OPENCV_AVAILABLE = False


class SaveImageEXR_Deployable:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "ComfyUI_EXR"})
            }
        }
    
    # MODIFIED: Added a STRING output for the file path
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    FUNCTION = "save_exr_images"
    OUTPUT_NODE = True
    CATEGORY = "Image/Deployable"

    def save_exr_images(self, images, filename_prefix="ComfyUI_EXR"):
        if not OPENCV_AVAILABLE:
            raise ImportError("OpenCV is required to save EXR files with this node.")

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        
        # ADDED: Variable to store the path of the first saved file
        first_file_path = ""

        for image in images:
            image_np = image.cpu().numpy()

            if image_np.dtype != np.float32:
                 image_np = image_np.astype(np.float32)

            file = f"{filename}_{counter:05}.exr"
            file_path = os.path.join(full_output_folder, file)
            
            # ADDED: Capture the path of the first image
            if not first_file_path:
                first_file_path = file_path

            image_np_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            cv2.imwrite(file_path, image_np_bgr)

            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        # MODIFIED: Return both the UI data and the direct file_path output
        return {"ui": {"images": results}, "result": (first_file_path,)}

# --- EXPORT FLOAT NODE (UNCHANGED) ---

class ExportFloat:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("FLOAT", {
                    "default": 0.0,
                    "min": -1e9,
                    "max": 1e9,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "number"
                }),
                "output_name": ("STRING", {"default": "float_output"}),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "export_value"

    CATEGORY = "Image/Deployable"

    def export_value(self, value, output_name):
        text_output = f"{output_name}: {value}"
        
        return {
            "ui": {
                "text": [text_output]
            },
            "result": (value,)
        }

# --- NODE REGISTRATION (UNCHANGED) ---

NODE_CLASS_MAPPINGS = {
    "SaveImageEXR_Deployable": SaveImageEXR_Deployable,
    "ExportFloat": ExportFloat
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageEXR_Deployable": "Save EXR (Deployable)",
    "ExportFloat": "Export Float"
}