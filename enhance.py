from realesrgan import RealESRGAN
import torch
from PIL import Image

device = torch.device('cpu')

model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x4.pth')

def enhance_image(image):
    image = image.convert("RGB")
    return model.predict(image)