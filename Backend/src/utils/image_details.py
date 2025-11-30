from pathlib import Path
import numpy as np
from PIL import Image


def get_info_from_image(image_path):
    image_path = str(image_path)
    filename = Path(image_path).name
    values = filename.split(" ")
    name = values[0]
    img_id = str(np.random.randint(1000000))  # removes extension
    
    usn = name+img_id
    img = Image.open(image_path).convert('RGB')
    return img, name, usn, img_id