import io
import torch
import numpy as np
from PIL import Image, ImageFile
import json
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_prediction(img_bytes, model):
    """
    Args:
        model: The trained model for keypoint detection.
    """
    image = Image.open(img_bytes)
    image = image.convert('L')  # convert image to greyscale
    image = image.resize((96, 96), Image.NEAREST)  # resize to 96x96

    image.save('debug_resized_image.png') # TODO: remove - debugging

    # Convert PIL image to PyTorch tensor
    image = torch.from_numpy(np.array(image))
    image = image / 255.0  # normalize to [0, 1]

    # Add an extra dimension for batch size and grayscale channel
    image = image.unsqueeze(0).unsqueeze(0)
    
    print("aa")
    
    # Get the keypoints
    keypoints = model(image)
    keypoints = torch.squeeze(keypoints).view(15, 2).detach().cpu().numpy()

    print("pierp")
    # Scale the keypoints back to the size of the original frame
    keypoints = keypoints * (image.size[0] / 96, image.size[1] / 96)
    
    # convert numpy array to list
    keypoints_list = keypoints.tolist()  

    # Convert list to JSON
    keypoints_json = json.dumps(keypoints_list)

    return keypoints_json
    