from PIL import Image
from pathlib import Path


def convert_image(image_to_convert_path: Path, output_directory_path: Path):
    '''
    Converts an input image to the required format for the e-paper display:
    - Rotates if in portrait orientation
    - Crops to a 5:3 aspect ratio from the center
    - Resizes to 800x480 pixels
    - Quantizes to the 6-color palette supported by the display
    @param image_to_convert_path: Path to the input image (can be any common format).
    @param output_directory_path: Directory where the converted image will be saved.
    '''

    if not output_directory_path.exists():
        print(f"Output directory not provided, exiting.")
        return

    img = Image.open(image_to_convert_path)
    file_name = image_to_convert_path.stem

    # Rotate if portrait
    # Needs to be vertical
    if img.height > img.width:
        img = img.rotate(90, expand=True)


    # Crop to 5:3 aspect ratio from center
    w, h = img.size
    target_ratio = 800 / 480  # = 5:3
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Image is too wide — crop sides
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Image is too tall — crop top and bottom
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    # Now resize to exact display resolution
    img = img.resize((800, 480))

    # Convert to the 6-color e-paper palette
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette([
        0, 0, 0,        # black
        255, 255, 255,  # white
        0, 255, 0,      # green
        0, 0, 255,      # blue
        255, 0, 0,      # red
        255, 255, 0,    # yellow
    ] + [0] * (256 - 6) * 3)

    img = img.quantize(palette=palette_img)
    img.save(f"{output_directory_path}/{file_name}.bmp")