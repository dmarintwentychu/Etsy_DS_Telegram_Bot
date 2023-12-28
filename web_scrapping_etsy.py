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
    rating = 0
    nReviews = 0
    nShopRating = 0
    description = ""
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
        self.search_rating(self.tree)
        self.search_nReviews(self.tree)
        self.search_nShopRating(self.tree)
        self.search_description(self.tree)

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
        else:
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

        if price_elem is not None:
            
            cadena_limpia = ''.join(c for c in price_elem[0].strip() if c.isdigit() or c in {',', '.'})

            cadena_limpia = cadena_limpia.replace(',', '.')

            self.shippingCosts =  float(cadena_limpia)
        else:

            self.shippingCosts =  False
    
    def search_rating(self,tree):

        link_element = tree.xpath('//a[@class="wt-text-link-no-underline review-stars-text-decoration-none" and @href="#reviews"]')

        if link_element is not None:
            span_element = link_element[0].xpath('.//span[@class="wt-screen-reader-only"]')
            if span_element:
                stars_text = span_element[0].text
                pat = r"[0-9](\.[0-9]+)?"
                self.rating = float(re.search(pat, stars_text).group(0))

    def search_nReviews(self,tree):
        
        reviews_elem = tree.xpath('//span[@class="wt-badge wt-badge--statusInformational wt-ml-xs-2"]')[0]

        if reviews_elem is not None:
            self.nReviews = int(reviews_elem.text)
        else:
            self.nReviews = False
    def search_nShopRating(self,tree):

        reviews_elem = tree.xpath('//span[@class="wt-badge wt-badge--statusInformational wt-ml-xs-2 wt-nowrap"]')[0]

        if reviews_elem is not None:
            self.nShopRating = int(reviews_elem.text)
        else:
            self.nShopRating = False
    def search_description(self,tree):

        self.description = tree.xpath('//h1[@class="wt-text-body-01 wt-line-height-tight wt-break-word wt-mt-xs-1"]')[0].text_content().strip()

        