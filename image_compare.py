import cv2
from PIL import Image
import pillow_avif
import numpy as np
import os

#Convierte todas las imágenes en jpg
def convert_images_to_jpg(input_folder, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        if os.path.isfile(input_path) and any(filename.lower().endswith(ext) for ext in ['.png', '.bmp', '.gif', '.tiff', '.jpeg', '.jpg', '.avif', '.webp']):
            try:
                img = Image.open(input_path)
                
                output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")
                img.convert('RGB').save(output_path, 'JPEG')

                print(f"Converted: {input_path} to {output_path}")
            except Exception as e:
                print(f"Error processing {input_path}: {e}")


#Compara dos imágenes y devuelve en % si son el mismo objeto o no (mas de un 60% suelen ser el mismo objeto)
def compare_images(image_path1, image_path2):

    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)

    matches = sorted(matches, key=lambda x: x.distance)
    
    print(len(matches))
    return (len(matches)*100) / 500


def deleteall(input_folder):

   for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        if os.path.isfile(input_path) and any(filename.lower().endswith(ext) for ext in ['.png', '.bmp', '.gif', '.tiff', '.jpeg', '.jpg', '.avif', '.webp']):
            os.remove(input_path)