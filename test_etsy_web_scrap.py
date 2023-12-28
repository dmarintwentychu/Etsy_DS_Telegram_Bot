from web_scrapping_etsy import etsyP

t = etsyP("https://www.etsy.com/es/listing/912901186/lion-stuffed-toy-amigurumi-lion-good?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=handmade+gift&ref=sr_gallery-1-14&pro=1&etp=1&organic_search_click=1")

print(f"Está hecho a mano? {t.isHM}")
print(f"Gastos de envio: {t.shippingCosts}")
print(f"Precio: {t.price}")
print(f"Precio Total {t.totalPriece}")

#print(is_hand_made(setwp("https://www.etsy.com/es/listing/1623298851/figura-de-estatua-de-one-piece-roronoa?click_key=858f33bdf5b0876eb96a4acc487b5409cfd4c295%3A1623298851&click_sum=ee803e7d&ref=hp_rv-1")))