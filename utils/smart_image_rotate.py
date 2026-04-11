from PIL import Image, ImageFilter, ImageOps
import numpy as np


def auto_rotate_to_vertical(img: Image.Image) -> Image.Image:
    """
    Return a portrait-oriented version of the image using a simple
    visual-weight heuristic.

    Rules:
    - If image is landscape, only 90 and 270 degrees are considered.
    - If image is portrait, only 0 and 180 degrees are considered.
    - If image is square, returns it unchanged.
    - Chooses the orientation whose visual "mass" is lower in the frame,
      which often makes the composition feel more grounded.

    The input image is not modified in place.
    """
    width, height = img.size

    if width == height:
        return img.copy()

    if height > width:
        candidate_angles = [0, 180]
    else:
        candidate_angles = [90, 270]

    scored = []
    for angle in candidate_angles:
        rotated = _rotate_image(img, angle)
        score = _vertical_composition_score(rotated)
        scored.append((score, angle, rotated))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_angle, best_img = scored[0]

    # Optional safety margin:
    # if the two options are nearly tied, keep the less-rotated choice.
    if len(scored) == 2 and abs(scored[0][0] - scored[1][0]) < 0.02:
        fallback_angle = 0 if height > width else 90
        for _, angle, rotated in scored:
            if angle == fallback_angle:
                return rotated

    return best_img


def _rotate_image(img: Image.Image, angle: int) -> Image.Image:
    """
    Rotate clockwise by angle in {0, 90, 180, 270}.
    Uses expand=True so dimensions are correct after rotation.
    """
    if angle == 0:
        return img.copy()
    if angle == 90:
        return img.transpose(Image.Transpose.ROTATE_270)  # Pillow rotates counterclockwise
    if angle == 180:
        return img.transpose(Image.Transpose.ROTATE_180)
    if angle == 270:
        return img.transpose(Image.Transpose.ROTATE_90)
    raise ValueError("angle must be one of 0, 90, 180, 270")


def _vertical_composition_score(img: Image.Image) -> float:
    """
    Score portrait image orientation.
    Higher score is better.

    Heuristic:
    - Use edge strength as visual weight.
    - Prefer lower center of mass (weight toward bottom).
    - Prefer weight near horizontal center.
    """
    gray = ImageOps.grayscale(img)

    # Edge map: finds structural detail that often correlates with "visual weight"
    edges = gray.filter(ImageFilter.FIND_EDGES)

    # Slight blur to reduce noise and isolated tiny edges
    edges = edges.filter(ImageFilter.GaussianBlur(radius=2))

    weights = np.asarray(edges, dtype=np.float32)

    total = weights.sum()
    if total <= 1e-6:
        return float("-inf")

    h, w = weights.shape
    ys, xs = np.indices((h, w), dtype=np.float32)

    cx = float((weights * xs).sum() / total) / max(w - 1, 1)
    cy = float((weights * ys).sum() / total) / max(h - 1, 1)

    # Higher cy is better: puts heavier content lower in the image.
    # Smaller |cx - 0.5| is better: keeps composition horizontally centered.
    score = 0.8 * cy - 0.2 * abs(cx - 0.5)
    return score