from PIL import Image

def convert_webp_to_png(image_path, output_path):
    # Open the webp image
    img = Image.open(image_path)

    # Save the image in png format
    img.save(output_path, 'PNG')

# Usage
convert_webp_to_png('assets/sprites/3.webp', 'assets/sprites/3.png')