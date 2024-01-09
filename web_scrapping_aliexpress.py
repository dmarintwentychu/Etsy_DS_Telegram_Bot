import re
import requests
from lxml import html
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import image_compare as ic
import spacy


class aliP:

    url = ""
    price = 0 
    content = ""
    shippingCosts = 0
    totalPriece = 0 #Con gastos de envío
    rating = 0
    nReviews = 0
    description = ""
    imgs = 0
    portrait = 0
    def __init__(self, url):
        self.url = url
        
    def download_img_ali(self,url):
        response = requests.get(url)

        if response.status_code != 200:
            self.tree =  False
        
        self.content = response.content
        pattern = r'"imagePathList":\s*\[([^]]*)\],\s*"image640PathList"'        
        exp = re.compile(pattern)
        urls_imagenes = (exp.findall(str(self.content))[0]
                         .replace("\"","")
                         .split(","))
        urls_imagenes = [url_imagene.strip() for url_imagene in urls_imagenes]

        i = 0
        for urll in urls_imagenes:
            urllib.request.urlretrieve(urll, f'./imgcacheali/img{i}.jpg')
            i+=1
        self.imgs = len(urls_imagenes)
        self.portrait = urls_imagenes[0]


    def get_values(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Ejecutar en modo sin cabeza
        driver = webdriver.Chrome(options=options)

        driver.get(self.url)

        try:
            driver.implicitly_wait(1)

            price_element = driver.find_element(By.XPATH, '//div[@class="es--wrap--erdmPRe notranslate"]')
        
            self.price = float(price_element.text
                               .replace("€","")
                               .replace(",","."))
        except NoSuchElementException:
            self.price = False

        try:            
            strong_element = driver.find_element(By.XPATH, '//div[@class="shipping--wrap--Dhb61O7"]//strong[contains(text(), "Envío:")]')

            shipping_info = strong_element.text
            
            self.shippingCosts = (shipping_info.split("Envío:")[1].split("€")[0]
                                            .strip()
                                            .replace(",","."))
        except NoSuchElementException:

            self.shippingCosts = False

        self.totalPriece = float(self.shippingCosts) + self.price

        try:            
            strong_element = driver.find_element(By.XPATH, '//div[@class="reviewer--wrap--sPGWrNq"]/strong')

            self.rating = float(strong_element.text)
        except NoSuchElementException:
            self.rating = False
        
        try:
            strong_element = driver.find_element(By.XPATH, '//a[@href="#nav-review"]')
            self.nReviews = (strong_element.text
                             .strip()
                             .split()[0])
        except NoSuchElementException:
            self.nReviews = False

        try:      
            strong_element = driver.find_element(By.XPATH, '//div[@class="title--wrap--Ms9Zv4A"]/h1')

            self.description = strong_element.text
        except NoSuchElementException:
            self.description = False
        
        driver.quit()
    
    def print(self):
        print("------------------------------------")
        print(f"Gastos de envio: {self.shippingCosts}")
        print(f"Precio: {self.price}")
        print(f"Precio Total {self.totalPriece}")
        print(f"Rating: {self.rating}")
        print(f"Numero de Reseñas del producto: {self.nReviews}")
        print(f"Descripción del Producto: \n {self.description}")
        print(f"url de aliexpress: {self.url}")
        print("------------------------------------")
    def message(self):
        message =(
f'''Gastos de envio: {self.shippingCosts}
Precio: {self.price}
Precio Total {self.totalPriece}
Rating: {self.rating}
Numero de Reseñas del producto: {self.nReviews}
Descripción del Producto: \n {self.description}
url de aliexpress: {self.url}''')
        
        return message

def getInfoProducts(links,etsy):
    
    aliPList = []
    for l in links:
        ali = aliP(l)
        ali.download_img_ali(ali.url)
        
        if getMatchProducts() > 1:
            aliPList.append(ali)
            aliPList[-1].get_values()
        ic.deleteall("./imgcacheali")

    ic.deleteall("./imgcacheetsy")

    if len(aliPList) == 0:
        if len(links >= 5):
            for l in links[:5]:
                ali = aliP(l)
                aliPList.append(ali)
                aliPList[-1].get_values()
        else:
            for l in links:
                ali = aliP(l)
                aliPList.append(ali)
                aliPList[-1].get_values()
 
    print(len(aliPList))

    return aliPList

def getMatchProducts():

    matches = 0    
    etimgl = ic.get_files_in_directory("./imgcacheetsy")
    alimgl = ic.get_files_in_directory("./imgcacheali")

    for e in etimgl:
        for a in alimgl:
            matches += ic.compare_images(e,a)

    return matches

def quitar_articulos(description):
    nlp = spacy.load("es_core_news_sm")

    doc = nlp(description)

    sustantivos = [token.text for token in doc if token.text.lower() not in ["el", "la", "los", "las", "un", "una", "unos", "unas","de", "aparición"]]

    nueva_oracion = " ".join(sustantivos)

    return nueva_oracion

def searchbar_format_Aliexpress(description):

    description = quitar_articulos(description)
    basic_url  = 'https://www.aliexpress.com/wholesale?catId=0&SearchText='
    basic_url = basic_url + description
    basic_url = basic_url.replace(" ", "%20")

    return basic_url

#Devuelve como máximo 60 links pero solo voy a coger 10
def get_url_products(description):

    url = searchbar_format_Aliexpress(description)
    #url = description

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    driver.implicitly_wait(8)

    actions = ActionChains(driver)

    for i in range(40):
        actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)
    link_elements = driver.find_elements(By.XPATH, "//a[@class='multi--container--1UZxxHY cards--card--3PJxwBm search-card-item']")

    link_hrefs = [element.get_attribute('href') for element in link_elements]

    return link_hrefs[:10]