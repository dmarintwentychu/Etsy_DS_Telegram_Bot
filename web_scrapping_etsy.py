import re
import requests
from lxml import html

class etsyP:

    url = ""
    tree = ""
    isHM = False
    price = 0 
    shippingCosts = 0
    totalPriece = 0 #Con gastos de envío
    stars = 0
    nReviews = 0
    nImgMatches = 0


    def __init__(self, url):
        self.url = url
        self.setTree(url)
        if self.tree is None:
            print("Error, no se ha encontrado la página")

        self.is_hand_made(self.tree)

        self.search_price(self.tree)
        self.search_Shipping_Costs(self.tree)
        self.totalPriece = self.price + self.shippingCosts

    def setTree(self,url):

        response = requests.get(url)

        if response.status_code != 200:
            self.tree =  False
        
        tree = html.fromstring(response.content)

        self.tree = tree


    def is_hand_made(self, tree):

        pattern = "Hecho a mano"
        
        if tree.xpath(f'//text()[contains(.,"{pattern}")]'):
            self.isHM = True
        self.isHM = False

    def search_price(self,tree):

        price_elem = tree.xpath('//div[@data-selector="price-only"]/p[@class="wt-text-title-larger wt-mr-xs-1 "]')

        if price_elem:
            
            cadena_limpia = ''.join(c for c in price_elem[0].text_content().split(":")[1] if c.isdigit() or c in {',', '.'})

            cadena_limpia = cadena_limpia.replace(',', '.')

            self.price =  float(cadena_limpia)
        else:

            price_elem = tree.xpath('//div[@data-selector="price-only"]/p[@class="wt-text-title-larger wt-mr-xs-1 wt-text-slime"]')

            if price_elem:
                
                cadena_limpia = ''.join(c for c in price_elem[0].text_content().split(":")[1] if c.isdigit() or c in {',', '.'})

                cadena_limpia = cadena_limpia.replace(',', '.')

                self.price = float(cadena_limpia)
            else:
                self.price = False


    def search_Shipping_Costs(self,tree):

        price_elem = tree.xpath('//div[@class="wt-ml-xs-1"]/span[@class="currency-value"]/text()')

        if price_elem:
            
            cadena_limpia = ''.join(c for c in price_elem[0].strip() if c.isdigit() or c in {',', '.'})

            cadena_limpia = cadena_limpia.replace(',', '.')

            self.shippingCosts =  float(cadena_limpia)
        else:

            self.shippingCosts =  False