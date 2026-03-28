from PIL import Image

img = Image.open("image.jpg")
img = img.resize((800, 480))  # Resize to display resolution

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
img.save("converted.bmp")