import os
import random
from PIL import Image, ImageOps
from datetime import datetime

base_image_path = '/Users/krishshah/Pictures/Wallpapers/base.jpg'  # Update this path
input_folder = '/Users/krishshah/Pictures/Wallpapers/Scrapbook'  # Replace with your folder path
output_folder = '/Users/krishshah/Pictures/Wallpapers/Current/'
output_name = 'scrapbook.jpg'

target_width = 400

def get_datetime_string():
    now = datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")

def load_images_from_folder(folder, base_image_path):
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    image_paths = [f for f in files if os.path.splitext(f)[1].lower() in supported_formats and f != base_image_path]
    return image_paths

def resize_and_add_border(image, scale_factor, border_size=5):
    # first we resize each image to be same width
    aspect_ratio = image.width / image.height
    new_height = int(target_width / aspect_ratio)

    # Resize image according to the scale factor
    new_size = (int(target_width * scale_factor), int(new_height * scale_factor))
    resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Add a black border
    bordered_image = ImageOps.expand(resized_image, border=border_size, fill='black')
    
    return bordered_image

def calculate_overlap(new_img_area, occupied_areas):
    new_x, new_y, new_w, new_h = new_img_area
    overlap_area = 0
    for occ_area in occupied_areas:
        occ_x, occ_y, occ_w, occ_h = occ_area
        overlap_width = min(new_x + new_w, occ_x + occ_w) - max(new_x, occ_x)
        overlap_height = min(new_y + new_h, occ_y + occ_h) - max(new_y, occ_y)
        if overlap_width > 0 and overlap_height > 0:
            overlap_area += overlap_width * overlap_height
    return overlap_area

def find_placement_for_image(img, occupied_areas, wallpaper_size):
    best_position = None
    min_overlap = float('inf')
    for attempt in range(100):  # Attempt placement 100 times to find a good position
        # Ensure x and y ranges are valid
        max_x = max(wallpaper_size[0] - img.width, 1)
        max_y = max(wallpaper_size[1] - img.height, 1)

        # Adjust to avoid ValueError by ensuring a valid range
        if max_x > 1 and max_y > 1:
            x = random.randint(0, max_x - 1)
            y = random.randint(0, max_y - 1)
            overlap = calculate_overlap((x, y, img.width, img.height), occupied_areas)
            if overlap < min_overlap:
                min_overlap = overlap
                best_position = (x, y)
        else:
            # If no valid position is found due to the image size, break and possibly log the issue or handle the image differently
            print(f"Image too large to fit: {img.width}x{img.height}")
            break

    return best_position

def create_wallpaper_with_base(base_image_path, input_folder, output_path, wallpaper_size=(1920, 1080), border_size=5):
    base_image = Image.open(base_image_path).resize(wallpaper_size)
    image_paths = load_images_from_folder(input_folder, base_image_path)
    images = [Image.open(path) for path in image_paths]

    wallpaper = base_image.copy()
    occupied_areas = []

    for img in images:
        scale_factor = random.uniform(0.5, 1.5)  # Adjust scaling factor as needed
        img = resize_and_add_border(img, scale_factor, border_size)

        position = find_placement_for_image(img, occupied_areas, wallpaper_size)
        if position:
            x, y = position
            wallpaper.paste(img, (x, y), img.convert('RGBA') if img.mode == 'RGBA' else None)
            occupied_areas.append((x, y, img.width, img.height))

    wallpaper.save(output_path)


output_path = output_folder + get_datetime_string() + output_name

# first we delete all images in the output folder that have "scrapbook" in the name
for file in os.listdir(output_folder):
    if output_name in file:
        os.remove(output_folder + file)

create_wallpaper_with_base(base_image_path, input_folder, output_path + get_datetime_string() + '.jpg')
