import torch
import torchvision.transforms as transforms
from PIL import Image
from .unet import UNet

def load_model(model_path='brats_final/unet_brain_tumor.pth'):
    model = UNet(in_channels=1, out_channels=1)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    return model

def preprocess_image(image_path):
    image = Image.open(image_path).convert('L')  # convert to grayscale
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])
    return transform(image).unsqueeze(0)  # shape: (1, 1, 256, 256)

def predict_segmentation(image_path):
    model = load_model()
    input_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(input_tensor)
    return output.squeeze().numpy()
