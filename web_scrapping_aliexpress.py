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

    return 

def get_url_Products(url):
    
    response = requests.get(url)

    if response.status_code != 200:
          return False
        
    tree = html.fromstring(response.content)

    return tree.xpath("//div[@class='list--galleryWrapper--29HRJT4']//a[@class='multi--container--1UZxxHY cards--card--3PJxwBm search-card-item']/@href")


    

p = get_url_Products("https://es.aliexpress.com/w/wholesale-Estatua-de-la-apariciónn-de-Zoro-Ashura.html")

print(len(p))
print(p)