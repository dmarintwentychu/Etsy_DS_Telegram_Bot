import web_scrapping_aliexpress as ali

url = 'https://www.aliexpress.com/wholesale?catId=0&SearchText='
all_products = ali.get_url_products(url, max_pages=3)
print(len(all_products))