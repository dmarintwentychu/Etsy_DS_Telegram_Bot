from web_scrapping_etsy import etsyP
import web_scrapping_aliexpress as ali

t = etsyP("https://www.etsy.com/es/listing/1535853173/estatua-de-la-aparicion-de-zoro-ashura?click_key=1ee745b1d04fd252598485a4cccea43d5a6522dc%3A1535853173&click_sum=3309dd3c&ref=hp_rv-2&frs=1")

print(f"Está hecho a mano? {t.isHM}")
print(f"Gastos de envio: {t.shippingCosts}")
print(f"Precio: {t.price}")
print(f"Precio Total {t.totalPriece}")
print(f"Rating: {t.rating}")
print(f"Numero de Reseñas del producto: {t.nReviews}")
print(f"Numero de Reseñas en la tienda: {t.nShopRating}")
print(f"Descripción del Producto: \n {t.description}")

print(ali.searchbar_Aliexpress(t.description))