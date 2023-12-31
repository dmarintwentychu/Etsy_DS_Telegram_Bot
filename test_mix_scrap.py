import web_scrapping_etsy as e
import web_scrapping_aliexpress as ali
from web_scrapping_etsy import etsyP
import image_compare as ic

t = etsyP("https://www.etsy.com/es/listing/1535853173/estatua-de-la-aparicion-de-zoro-ashura?click_key=3694a72da918749fef41800d3bc29e67dba9d0df%3A1535853173&click_sum=36d9f1a5&ref=hp_rv-5&frs=1")

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