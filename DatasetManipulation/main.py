import os
import random
import math
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Define input and output directories
input_dir = 'input'
output_dir = 'output'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)


# Function to convert RGBA to RGB if needed
def convert_to_rgb(image):
    if image.mode == 'RGBA':
        return image.convert('RGB')
    return image


# Function to apply a wavy distortion
def apply_wave_distortion(image):
    width, height = image.size
    pixels = image.load()
    output_image = Image.new('RGB', (width, height))
    output_pixels = output_image.load()

    # Parameters for wave effect
    amplitude = random.randint(5, 30)  # Amplitude of the wave
    frequency = random.uniform(0.05, 0.15)  # Frequency of the wave

    for x in range(width):
        for y in range(height):
            # Apply sinusoidal wave to the vertical position of each pixel
            new_y = int(y + amplitude * math.sin(2 * math.pi * frequency * x))
            if new_y >= 0 and new_y < height:
                output_pixels[x, new_y] = pixels[x, y]

    return output_image


# Function to apply various transformations
def transform_image(image, image_name, output_dir):
    # Ensure the image is in RGB format
    image = convert_to_rgb(image)

    # Save original (upright)
    image.save(os.path.join(output_dir, f'{image_name}_original.jpg'))

    # Resize (more extreme stretch/shrink) - Random width and height between 50% and 150% of original size
    width, height = image.size
    new_width = random.randint(int(0.5 * width), int(1.5 * width))
    new_height = random.randint(int(0.5 * height), int(1.5 * height))
    resized = image.resize((new_width, new_height))
    resized.save(os.path.join(output_dir, f'{image_name}_resized_{new_width}x{new_height}.jpg'))

    # Apply a strong wave distortion
    wave_distorted = apply_wave_distortion(image)
    wave_distorted.save(os.path.join(output_dir, f'{image_name}_wave_distorted.jpg'))

    # Change brightness randomly (even more extreme)
    enhancer_brightness = ImageEnhance.Brightness(image)
    brightness_factor = random.uniform(0.3, 2.0)  # Random brightness between 30% and 200%
    brightened = enhancer_brightness.enhance(brightness_factor)
    brightened.save(os.path.join(output_dir, f'{image_name}_brightness_{brightness_factor:.2f}.jpg'))

    # Change contrast randomly (more extreme)
    enhancer_contrast = ImageEnhance.Contrast(image)
    contrast_factor = random.uniform(0.3, 2.0)  # Random contrast between 30% and 200%
    contrasted = enhancer_contrast.enhance(contrast_factor)
    contrasted.save(os.path.join(output_dir, f'{image_name}_contrast_{contrast_factor:.2f}.jpg'))

    # Add noise (stronger random pixel variations)
    def add_noise(img):
        noise_img = img.copy()
        pixels = noise_img.load()
        for i in range(noise_img.size[0]):
            for j in range(noise_img.size[1]):
                noise_factor = random.randint(-50, 50)  # Larger noise range
                r, g, b = pixels[i, j]
                pixels[i, j] = (max(0, min(255, r + noise_factor)),
                                max(0, min(255, g + noise_factor)),
                                max(0, min(255, b + noise_factor)))
        return noise_img

    noisy_image = add_noise(image)
    noisy_image.save(os.path.join(output_dir, f'{image_name}_noisy.jpg'))

    # Add stronger color distortion (modify hue/saturation)
    enhancer_color = ImageEnhance.Color(image)
    color_factor = random.uniform(0.3, 2.0)  # Random color enhancement between 30% and 200%
    color_distorted = enhancer_color.enhance(color_factor)
    color_distorted.save(os.path.join(output_dir, f'{image_name}_color_{color_factor:.2f}.jpg'))

    # Apply a stronger blur for more noticeable effect
    blurred = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(1.0, 5.0)))  # Larger blur radius
    blurred.save(os.path.join(output_dir, f'{image_name}_blurred.jpg'))


# Loop through all images in the input directory and apply transformations
for filename in os.listdir(input_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # Only process image files
        image_path = os.path.join(input_dir, filename)
        with Image.open(image_path) as img:
            image_name = os.path.splitext(filename)[0]  # Get the base filename without extension
            transform_image(img, image_name, output_dir)

print("Image transformation with drastic changes completed.")