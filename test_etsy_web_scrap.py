from web_scrapping_etsy import etsyP

t = etsyP("https://www.etsy.com/es/listing/1581587356/sudadera-con-capucha-hollow-knight-de?click_key=f589164a98f6a93900d4856977ab0a977b8d1042%3A1581587356&click_sum=0ca073c4&ref=landingpage_similar_listing_bot-4&pro=1&sts=1&listing_id=1581587356&listing_slug=sudadera-con-capucha-hollow-knight-de")

print(f"Está hecho a mano? {t.isHM}")
print(f"Gastos de envio: {t.shippingCosts}")
print(f"Precio: {t.price}")
print(f"Precio Total {t.totalPriece}")
print(f"Rating: {t.rating}")
print(f"Numero de Reseñas: {t.nReviews}")
print(f"Numero de Reseñas en la tienda {t.nShopRating}")
print(f"Descripción del Producto: \n {t.description}")

