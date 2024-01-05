from web_scrapping_etsy import etsyP
import web_scrapping_aliexpress as ali

t = etsyP("https://www.etsy.com/es/listing/1561713674/regalos-para-fanaticos-del-anime?click_key=cd148e36e716f1547531ff1422489df8aa7acfba%3A1561713674&click_sum=0eee9798&ref=sim_strv-6&pro=1&frs=1")

print(f"Está hecho a mano? {t.isHM}")
print(f"Gastos de envio: {t.shippingCosts}")
print(f"Precio: {t.price}")
print(f"Precio Total {t.totalPriece}")
print(f"Rating: {t.rating}")
print(f"Numero de Reseñas del producto: {t.nReviews}")
print(f"Numero de Reseñas en la tienda: {t.nShopRating}")
print(f"Descripción del Producto: \n {t.description}")

print(ali.searchbar_format_Aliexpress(t.description))