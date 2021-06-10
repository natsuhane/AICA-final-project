
"""
# Background remove tool.
# Module Version: 3.0 [Public]
# Rewrited by Anodev. (https://github.com/OPHoperHPO)
# Original source code: https://github.com/susheelsk/image-background-removal
"""
import os
import tqdm
import numpy as np
from PIL import Image
from io import BytesIO
from .deeplabmodel import DeepLabModel


class RemoveBackground:
    def __init__(self, player_input, player_output):
        """CLI"""
        print(os.path.dirname(__file__))
        # Parse arguments
        input_path = os.path.dirname(__file__) + '/Capture/' + player_input
        output_path = os.path.dirname(__file__) + '/Capture/' +  player_output
        model = DeepLabModel("xception_model")  # Init model
        jpeg_str = open(input_path, "rb").read()
        image = Image.open(BytesIO(jpeg_str))
        seg_map = model.run(image)
        image = image.convert('RGB')
        # Get image size
        width, height = image.size
        dummy_img = np.zeros([height, width, 4], dtype=np.uint8)
        for x in range(width):
            for y in range(height):
                color = seg_map[y, x]
                (r, g, b) = image.getpixel((x, y))
                if color == 0:
                    dummy_img[y, x, 3] = 0
                else:
                    dummy_img[y, x] = [r, g, b, 255]
        img = Image.fromarray(dummy_img)
        img.save(output_path)



