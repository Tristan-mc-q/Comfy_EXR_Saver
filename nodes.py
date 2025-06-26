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
    
    RETURN_TYPES = ()
    FUNCTION = "save_exr_images"
    OUTPUT_NODE = True
    CATEGORY = "Image/Deployable" # Let's put it in a custom category

    def save_exr_images(self, images, filename_prefix="ComfyUI_EXR"):
        if not OPENCV_AVAILABLE:
            # If opencv isn't installed, we can't proceed.
            raise ImportError("OpenCV is required to save EXR files with this node.")

        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()

        for image in images:
            image_np = image.cpu().numpy()

            # Ensure image is in float32 format, which is standard for HDR/EXR
            if image_np.dtype != np.float32:
                 image_np = image_np.astype(np.float32)

            # Define the file path
            file = f"{filename}_{counter:05}.exr"
            file_path = os.path.join(full_output_folder, file)

            # OpenCV expects BGR color order, but ComfyUI tensors are RGB.
            # So we must convert the color channels before saving.
            image_np_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            # Save the image using OpenCV
            cv2.imwrite(file_path, image_np_bgr)

            # Append the result for the ComfyUI/ComfyDeploy backend
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        # Return the data in the format ComfyDeploy expects
        return {"ui": {"images": results}}