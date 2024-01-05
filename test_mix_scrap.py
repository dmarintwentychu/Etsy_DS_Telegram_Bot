import web_scrapping_etsy as e
import web_scrapping_aliexpress as ali
from web_scrapping_etsy import etsyP
import image_compare as ic
import time


t = time.time
t = etsyP("https://www.etsy.com/es/listing/1535853173/estatua-de-la-aparicion-de-zoro-ashura")

print(f"Está hecho a mano? {t.isHM}")
print(f"Gastos de envio: {t.shippingCosts}")
print(f"Precio: {t.price}")
print(f"Precio Total {t.totalPriece}")
print(f"Rating: {t.rating}")
print(f"Numero de Reseñas del producto: {t.nReviews}")
print(f"Numero de Reseñas en la tienda: {t.nShopRating}")
print(f"Descripción del Producto: \n {t.description}")

print(ali.searchbar_format_Aliexpress(t.description))

links = ali.get_url_products(t.description)

aliPList = ali.getInfoProducts(links,t)
for a in aliPList:
    a.print()

print(time.time - t)