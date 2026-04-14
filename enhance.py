from PIL import Image, ImageEnhance, ImageFilter

def enhance_image(image):
    image = image.convert("RGB")

    # Sharpen
    image = image.filter(ImageFilter.SHARPEN)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    # Increase sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)

    return image