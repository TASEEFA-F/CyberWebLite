from PIL import Image
import numpy as np

def encode_message(image_path, message, output_path="stego.png"):
    img = Image.open(image_path).convert("RGB")
    data = np.array(img)
    flat = data.flatten()

    message += "##"  # EOF marker
    binary = ''.join(format(ord(c), '08b') for c in message)

    if len(binary) > len(flat):
        raise ValueError("Message too long for this image.")

    for i in range(len(binary)):
        flat[i] = (flat[i] & 0b11111110) | int(binary[i])

    encoded = flat.reshape(data.shape)
    Image.fromarray(encoded.astype('uint8')).save(output_path)

def decode_message(image_path):
    img = Image.open(image_path).convert("RGB")
    data = np.array(img).flatten()

    binary = ''.join(str(pixel & 1) for pixel in data)
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    message = ''.join(chars)
    return message.split("##")[0]