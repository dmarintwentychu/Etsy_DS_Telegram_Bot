import web_scrapping_aliexpress as ali

url = 'https://www.aliexpress.com/wholesale?catId=0&SearchText=zoro%20roronoa'
all_products = ali.get_url_products(url, max_pages=3)
print(all_products[3])

