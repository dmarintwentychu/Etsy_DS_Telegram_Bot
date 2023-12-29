import re
import requests
from lxml import html

class aliP:

    url = ""
    tree = ""
    price = 0 
    shippingCosts = 0
    totalPriece = 0 #Con gastos de envío
    rating = 0
    nReviews = 0
    images = []

    def setTree(self,url):

        response = requests.get(url)

        if response.status_code != 200:
            self.tree =  False
        
        tree = html.fromstring(response.content)

        self.tree = tree


def searchbar_Aliexpress(description):
    
    basic_url  = 'https://www.aliexpress.com/wholesale?catId=0&SearchText='
    basic_url = basic_url + description
    basic_url = basic_url.replace(" ", "%20")

    return basic_url

#Devuelve como máximo max_pages*10 links
def get_url_products(url, max_pages=1):
    all_links = []

    for page in range(1, max_pages + 1):
        current_url = f"{url}&page={page}"  # Ajusta esto según la estructura de la URL con paginación

        response = requests.get(current_url)

        if response.status_code != 200:
            print(f"Error en la solicitud para la página {page}: {response.status_code}")
            break

        pattern = 'href="(//es\.aliexpress\.com/item/.*?)"'
        exp = re.compile(pattern)

        links = exp.findall(str(response.content))
        all_links.extend(links)

    return all_links

