from PIL import Image

# ASCII characters used to represent pixel intensity
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)  # 0.55 to adjust for console aspect ratio
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")  # convert to grayscale

def pixels_to_ascii(image):
    pixels = image.getdata()
    chars = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return chars

def image_to_ascii(image_path, new_width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image: {e}")
        return

    image = resize_image(image, new_width)
    image = grayify(image)
    
    ascii_str = pixels_to_ascii(image)
    
    # Format the string into lines
    ascii_lines = [ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)]
    ascii_image = "\n".join(ascii_lines)
    
    print(ascii_image)

# Example usage
image_to_ascii("svampbob.webp", new_width=100)
