import re
import requests
import urllib.request
from lxml import html

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

import schedule
import json

class etsyP:

    url = ""
    driver = 0
    content = ""
    isHM = False
    price = 0 
    shippingCosts = 0
    totalPriece = 0 #Con gastos de envío
    rating = 0
    nReviews = 0
    nShopRating = 0
    description = ""
    imgs = 0
    ImgMatches = 0
    

    def __init__(self, url,t=0):
        self.url = url
                

        block = True
        while(block):
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-gpu')
                #options.add_argument('--headless')

                self.driver = webdriver.Chrome(options=options)

                wait = WebDriverWait(self.driver, 5)
                self.driver.get(self.url)
                self.driver.minimize_window()
                self.driver.implicitly_wait(2)
                self.driver.refresh()
                self.driver.implicitly_wait(2)
                boton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='wt-btn wt-btn--filled wt-mb-xs-0']")))
                boton.click()
                block = False
            except TimeoutException:
                print("Captcha 😡")
                self.driver.quit()

        if t == 0:
            self.is_hand_made()
            self.search_price()
            self.search_Shipping_Costs()
            self.totalPriece = self.price + self.shippingCosts
            self.search_rating()
            self.search_nReviews()
            self.search_nShopRating()
            self.search_description()
            self.download_img_etsy()
        else:
            self.search_price()
            self.search_Shipping_Costs()
            self.totalPriece = self.price + self.shippingCosts

        self.driver.quit()

    def is_hand_made(self):
        pattern = "Hecho a mano"
        
        try:
            self.driver.find_element(By.XPATH, f'//*[contains(text(), "{pattern}")]')
            self.isHM = True
        except NoSuchElementException:
            # Si no se encuentra el elemento, establece isHM en False
            self.isHM = False

    def search_price(self):

        xpath_condition_1 = '//div[@data-selector="price-only"]/p[@class="wt-text-title-larger wt-mr-xs-1 "]'
        xpath_condition_2 = '//div[@data-selector="price-only"]/p[@class="wt-text-title-larger wt-mr-xs-1 wt-text-slime"]'
        
        try:
            price_elem = self.driver.find_element(By.XPATH,xpath_condition_1)
        except:
            price_elem = self.driver.find_element(By.XPATH,xpath_condition_2)

        if price_elem:
            cadena_limpia = self.extract_price_from_element(price_elem.text)
            self.price = float(cadena_limpia)
        else:
            self.price = False

    def extract_price_from_element(self, element):
        cadena_limpia = ''.join(c for c in element.strip().split(":")[1] if c.isdigit() or c in {',', '.'})
        return cadena_limpia.replace(',', '.')
    
    def search_Shipping_Costs(self):

        try:
            price_elem = self.driver.find_element(By.XPATH,'//div[@class="wt-ml-xs-1"]/span[@class="currency-value"]/text()')
            
            cadena_limpia = ''.join(c for c in price_elem[0].strip() if c.isdigit() or c in {',', '.'})

            cadena_limpia = cadena_limpia.replace(',', '.')

            self.shippingCosts =  float(cadena_limpia)
        except:
            self.shippingCosts =  False
    
    def search_rating(self):
        
        link_element = self.driver.find_element(By.XPATH,'//a[@class="wt-text-link-no-underline review-stars-text-decoration-none" and @href="#reviews"]')
        #link_element = self.tree.xpath('//a[@class="wt-text-link-no-underline review-stars-text-decoration-none" and @href="#reviews"]')
        pat = r"[0-9](\.[0-9]+)?"
        self.rating = float(re.search(pat, link_element.text).group(0))

    def search_nReviews(self):
        
        try:
            reviews_elem = self.driver.find_element(By.XPATH,'//span[@class="wt-badge wt-badge--statusInformational wt-ml-xs-2"]')
            self.nReviews = reviews_elem.text
        except:
            self.nReviews = False

    def search_nShopRating(self):
        
        try:
            reviews_elem = self.driver.find_element(By.XPATH,'//div[@class="reviews__shop-info"]')
            self.nShopRating = float(reviews_elem.text.split()[0])
        except:
            self.nShopRating = False

    def search_description(self):

        self.description = self.driver.find_elements(By.XPATH,'//div[@class="wt-mb-xs-1"]/h1[@class="wt-text-body-01 wt-line-height-tight wt-break-word wt-mt-xs-1"]')[0].text

    def download_img_etsy(self):

        imagenes = self.driver.find_elements(By.XPATH, '//div[@id="photos"]//img')

        urls_imagenes = [imagen.get_attribute("src") for imagen in imagenes]

        urls_imagenes = urls_imagenes[:len(urls_imagenes)//2]
        i = 0
        for url in urls_imagenes:
            urllib.request.urlretrieve(url, f'./imgcacheetsy/img{i}.jpg')
            i += 1

        self.imgs = len(urls_imagenes)


#Añade un nuevo producto
def trackNewProduct(url):

    p = etsyP(url,1)

    with open('./products.json',"r+") as f:
        
        z = json.load(f)

        dictionary = {f"{url}" : p.totalPriece}

        z.update(dictionary)

        f.seek(0)
        json.dump(z,f,indent=2)
        f.truncate()

#0:No cambia
#1:Ha bajado
#2:Ha subido
def trackProduct(url,f,z):
    
    res = 0
    lastPrice = z[url]
    p = etsyP(url,1)

    if lastPrice < p.totalPriece:
        res = 1
    elif lastPrice > p.totalPriece:
        res = 2
    else:
        res = 0
    z[url] = p.totalPriece

    f.seek(0)
    f.truncate()
    json.dump(z,f,indent=2)


    return (res,p.totalPriece)

def deleteJSON():
    with open('./archivo.json', 'w') as f:
        f.write('{}')


#Mira entre todos los productos añadidos y devuelve tres diccionarios diciendo si ha suvbido, bajado o sigue igual
def trackListProducts():

    lowered = {}
    raised = {}
    equal = {}

    with open('./products.json',"r+") as f:
        
        z = json.load(f)
        keys = list(z.keys())
        for url in keys:
            (r,p) = trackProduct(url,f,z)
            
            if r == 0:
                equal[url] = p
            elif r == 1:
                lowered[url] = p
            else:
                equal[url] = p

    return (lowered, raised, equal)



#Esto estaría en el main
#def job():
#    print("Ejecutando la tarea...")
#    (lowered, raised, equal) = trackListProducts()
    
#schedule.every().hour.do(job)

