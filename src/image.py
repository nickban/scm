from PIL import Image
import os
 

 # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


input_folder = os.path.join(BASE_DIR, 'src/media/order/avatar/')
output_folder = os.path.join(BASE_DIR, 'src/media/order/avatar1/')
new_size = (100, 100)
 
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        with Image.open(os.path.join(input_folder, filename)) as im:
            im.thumbnail(new_size)
            im.save(os.path.join(output_folder, filename))