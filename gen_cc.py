import pycountry
from PIL import Image, ImageDraw, ImageFont
import os

def create_country_code_sticker(country_code, size=(300, 200), bg_color='white', text_color='black', font_name='Arial Bold'):
    # Create a new image at a higher resolution
    scale_factor = 4
    large_size = (size[0] * scale_factor, size[1] * scale_factor)
    img = Image.new('RGB', large_size, bg_color)
    draw = ImageDraw.Draw(img)

    # Draw an oval inside the image at the higher resolution to create the border
    border_width = 10 * scale_factor  # Scale up the border width as well
    draw.ellipse([border_width, border_width, large_size[0] - border_width, large_size[1] - border_width], outline=text_color, width=border_width)

    # Load font (try to use Arial Black or fallback to default font)
    try:
        # Attempt to load Arial Black by name
        font = ImageFont.truetype(font_name, size=int(large_size[1] * 0.6))  # Scale up the font size
    except IOError:
        # Fallback to the default font if Arial Black is not found
        print("Arial Black font not found. Using default font.")
        font = ImageFont.load_default()

    # Calculate text size and position at the higher resolution
    ascent, descent = font.getmetrics()
    text_width, text_height = draw.textlength(country_code, font=font), ascent + descent
    text_x = (large_size[0] - text_width) / 2
    text_y = (large_size[1] - text_height) / 2

    # Draw the country code centered in the oval
    draw.text((text_x, text_y), country_code, font=font, fill=text_color)

    # Resize the image back down to the intended size for anti-aliasing effect
    img = img.resize(size, Image.LANCZOS)  # Use Image.LANCZOS for high-quality downscaling

    return img

output_dir = 'cc_imgs'
os.makedirs(output_dir, exist_ok=True)

countries = list(pycountry.countries)
for country in countries:
    country_code = country.alpha_2
    img = create_country_code_sticker(country_code)
    output_path = os.path.join(output_dir, f'{country_code}.png')
    img.save(output_path)
    print(f'Saved graphic for {country_code}')
