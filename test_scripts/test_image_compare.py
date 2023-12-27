import image_compare as im

im.convert_images_to_jpg("./imgtest/","./imgtest/")

image1_path = "./imgtest/zoro.jpg"
image2_path = "./imgtest/zoro2.jpg"
result = im.compare_images(image1_path, image2_path)


print(f"Las imágenes contienen el mismo objeto en un {result}% de acierto")

im.deleteall("./")