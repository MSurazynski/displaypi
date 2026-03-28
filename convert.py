from PIL import Image

img = Image.open("cycle_images_source/image.jpg")

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

# Optional: convert to the 6-color e-paper palette
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
img.save("cycle_images_converted/converted.bmp")