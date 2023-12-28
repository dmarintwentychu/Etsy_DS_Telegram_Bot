import image_compare as im

im.convert_images_to_jpg("./imgtest/","./imgtest/")

image1_path = "./imgtest/test2.jpg"
image2_path = "./imgtest/test1.jpg"
result = im.compare_images(image1_path, image2_path)
similarity = im.compare_images_color_histogram(image1_path,image2_path)

print(f"Las imágenes contienen el mismo objeto en un {result} % de acierto usando ORB")
print("Similitud entre los histogramas de color:", similarity)

#im.deleteall("./imgtest/")