import io
import cv2
import torch
import numpy as np
from PIL import Image

# from PIL import ImageFile
#ImageFile.LOAD_TRUNCATED_IMAGES = True
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#from numpy import expand_dims
#from werkzeug.utils import secure_filename
#from backend.utils import show_all_keypoints

def draw_keypoints(frame, keypoints):
    for keypoint in keypoints:
        x, y = keypoint
        cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)  # draw a green circle at each keypoint
    return frame

def get_prediction(img_bytes, model):
    """
    Args:
        img_bytes (bytes): The image bytes.
        model: The trained model for keypoint detection.

    Returns:
        bytes: The image bytes with keypoints drawn on it.
    """
    og_image = Image.open(img_bytes)
    image = og_image.convert('L')  # convert image to greyscale
    image = image.resize((96, 96))  # resize to 96x96

    # Convert PIL image to PyTorch tensor
    image = torch.from_numpy(np.array(image))
    image = image / 255.0  # normalize to [0, 1]
    
    # Add an extra dimension for batch size and grayscale channel
    image = image.unsqueeze(0).unsqueeze(0)
    
    # Get the keypoints
    keypoints = model(image)
    keypoints = keypoints.view(15, 2).detach().numpy()

    # Scale the keypoints back to the size of the original frame
    keypoints = keypoints * (og_image.size[0] / 96, og_image.size[1] / 96)

    # Draw the keypoints on the frame
    og_image_np = np.array(og_image)
    keypoint_img = draw_keypoints(og_image_np, keypoints)

    # Convert the numpy array back to a PIL Image
    processed_image = Image.fromarray(keypoint_img)

    # Save the PIL Image to a BytesIO object
    image_bytes = io.BytesIO()
    processed_image.save(image_bytes, format='PNG')

    # Get the bytes from the BytesIO object
    image_bytes = image_bytes.getvalue()

    return image_bytes
    