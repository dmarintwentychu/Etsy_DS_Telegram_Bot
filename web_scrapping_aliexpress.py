import re
import requests
from lxml import html

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request

class aliP:

    url = ""
    price = 0 
    shippingCosts = 0
    totalPriece = 0 #Con gastos de envío
    rating = 0
    nReviews = 0
    images = []

    def __init__(self, url):
        self.url = url

        self.get_values()
        #self.search_Shipping_Costs()
        #self.totalPriece = self.price + self.shippingCosts
        #self.search_rating()
        #self.search_nReviews()
        #self.search_nShopRating()
        #self.search_description()
        #self.download_img_ali()


    def download_img_ali(self):
        
        pattern = r'"imagePathList":\s*\[([^]]*)\],\s*"image640PathList"'        
        exp = re.compile(pattern)
        urls_imagenes = exp.findall(str(self.content))[0].replace("\"","").split(",")
        urls_imagenes = [url_imagene.strip() for url_imagene in urls_imagenes]
        
        i = 0
        for url in urls_imagenes:
            urllib.request.urlretrieve(url, f'./imgcacheali/img{i}.jpg')
            i+=1
    
    
    def get_values(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Ejecutar en modo sin cabeza
        driver = webdriver.Chrome(options=options)

        driver.get(self.url)

        driver.implicitly_wait(2)

        price_element = driver.find_element(By.XPATH, '//div[@class="es--wrap--erdmPRe notranslate"]')
        
        self.price = float(price_element.text.replace("€","").replace(",","."))

        driver.implicitly_wait(2)

        try:
            strong_element = driver.find_element(By.XPATH, '//div[@class="shipping--wrap--Dhb61O7"]//strong[contains(text(), "Envío:")]')

            shipping_info = strong_element.text

            
            self.shippingCosts = (shipping_info.split("Envío:")[1].split("€")[0]
                                            .strip().replace(",","."))

        except NoSuchElementException:
            # Si no se encuentra el elemento, imprimir un mensaje indicando que no se encontró
            print("No se encontró el elemento de envío.")
            self.shippingCosts = False
        
        driver.quit()


ali = aliP("https://es.aliexpress.com/item/1005004549580517.html?spm=a2g0o.detail.0.0.6821gSwRgSwR1Y&gps-id=pcDetailTopMoreOtherSeller&scm=1007.40000.327270.0&scm_id=1007.40000.327270.0&scm-url=1007.40000.327270.0&pvid=8fbba2f6-d6f6-4780-9c6e-86e26c7415f6&_t=gps-id:pcDetailTopMoreOtherSeller,scm-url:1007.40000.327270.0,pvid:8fbba2f6-d6f6-4780-9c6e-86e26c7415f6,tpp_buckets:668%232846%238113%231998&pdp_npi=4%40dis%21EUR%215.39%215.39%21%21%215.83%21%21%40211b618e17038634812338943e9302%2112000029575396713%21rec%21ES%214776018355%21AB&search_p4p_id=202312290724413987365388586586647121_2#nav-specification")

def getInfoProducts(links):

    aliPList = []

    for i in range(len(links)):
        aliPList[i] = aliP(links[i])

    return aliPList


def searchbar_format_Aliexpress(description):
    
    basic_url  = 'https://www.aliexpress.com/wholesale?catId=0&SearchText='
    basic_url = basic_url + description
    basic_url = basic_url.replace(" ", "%20")

    return basic_url

#Devuelve como máximo max_pages*10 links lo suyo es 2 páginas
def get_url_products(description, max_pages=1):

    url = searchbar_format_Aliexpress(description)

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

