from PIL import Image
from pathlib import Path



def convert_image(image_to_convert_path: Path, output_directory_path: Path, use_smart_rotation: bool = False):
    '''
    Converts an input image to the required format for the e-paper display:
    - Rotates to portrait orientation if needed
    - Crops to a vertical 3:5 aspect ratio from the center
    - Resizes to 480x800 pixels
    - Quantizes to the 6-color palette supported by the display
    @param image_to_convert_path: Path to the input image (can be any common format).
    @param output_directory_path: Directory where the converted image will be saved.
    @param use_smart_rotation: Whether to use smart rotation based on visual weight.
    '''

    output_directory_path.mkdir(parents=True, exist_ok=True)

    img = Image.open(image_to_convert_path)
    file_name = image_to_convert_path.stem
    output_width = 480
    output_height = 800

    # Ensure the image is vertical (portrait).
    if use_smart_rotation:
        from utils.smart_image_rotate import auto_rotate_to_vertical
        img = auto_rotate_to_vertical(img)
    if img.width > img.height:
        img = img.rotate(90, expand=True)

    # Crop to vertical 3:5 (width:height) from center.
    w, h = img.size
    target_ratio = output_width / output_height
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Image is too wide, crop left and right.
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Image is too tall, crop top and bottom.
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    # Now resize to exact display resolution
    img = img.resize((output_width, output_height))

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

    if img.width != output_width or img.height != output_height:
        raise ValueError(f"Final image has incorrect dimensions: {img.size}, expected {(output_width, output_height)}")

    img.save(output_directory_path / f"{file_name}.bmp")