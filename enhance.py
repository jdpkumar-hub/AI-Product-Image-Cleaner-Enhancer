from PIL import Image, ImageEnhance, ImageFilter
from rembg import remove
import io

def enhance_image(image):
    image = image.convert("RGB")

    # ---------- REMOVE BACKGROUND ----------
    input_bytes = io.BytesIO()
    image.save(input_bytes, format="PNG")
    output_bytes = remove(input_bytes.getvalue())

    image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # ---------- WHITE BACKGROUND ----------
    white_bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
    image = Image.alpha_composite(white_bg, image).convert("RGB")

    # ---------- ENHANCEMENTS ----------
    image = image.filter(ImageFilter.SHARPEN)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.4)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.8)

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.1)

    return image