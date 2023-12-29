import web_scrapping_etsy as e
import web_scrapping_aliexpress as ali
from web_scrapping_etsy import etsyP

t = etsyP("https://www.etsy.com/es/listing/1562368070/regalos-para-fanaticos-del-anime?click_key=c733a327d23a50d1a38f5e1efb023d5772619fbd%3A1562368070&click_sum=105d4d63&ref=internal_similar_listing_bot-3&pro=1&frs=1&listing_id=1562368070&listing_slug=regalos-para-fanaticos-del-anime")

print(f"Está hecho a mano? {t.isHM}")
print(f"Gastos de envio: {t.shippingCosts}")
print(f"Precio: {t.price}")
print(f"Precio Total {t.totalPriece}")
print(f"Rating: {t.rating}")
print(f"Numero de Reseñas del producto: {t.nReviews}")
print(f"Numero de Reseñas en la tienda: {t.nShopRating}")
print(f"Descripción del Producto: \n {t.description}")

print(ali.searchbar_format_Aliexpress(t.description))

links = ali.get_url_products(t.description, max_pages=2)
ali.getInfoProducts(links)