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

class aliP:

    url = ""
    price = 0 
    shippingCosts = 0
    totalPriece = 0 #Con gastos de envío
    rating = 0
    nReviews = 0

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

        try:
            driver.implicitly_wait(2)

            price_element = driver.find_element(By.XPATH, '//div[@class="es--wrap--erdmPRe notranslate"]')
        
            self.price = float(price_element.text.replace("€","").replace(",","."))

        except NoSuchElementException:
            self.price = False

        try:            
            strong_element = driver.find_element(By.XPATH, '//div[@class="shipping--wrap--Dhb61O7"]//strong[contains(text(), "Envío:")]')

            shipping_info = strong_element.text

            
            self.shippingCosts = (shipping_info.split("Envío:")[1].split("€")[0]
                                            .strip().replace(",","."))

        except NoSuchElementException:

            self.shippingCosts = False

        try:            
            strong_element = driver.find_element(By.XPATH, '//div[@class="reviewer--wrap--sPGWrNq"]/strong')

            self.rating = float(strong_element.text)
            
        except NoSuchElementException:
            self.rating = False
        
        try:
            strong_element = driver.find_element(By.XPATH, '//a[@href="#nav-review"]')
            self.nReviews = strong_element.text.strip().split()[0]
            
        except NoSuchElementException:
            self.nReviews = False


        driver.quit()


#ali = aliP("https://es.aliexpress.com/item/1005005878900854.html?spm=a2g0o.tm1000003765.3832216530.3.3bc638f2mLBOyn&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22sku_id%22:%2212000035739136644%22%7D&scm=1007.39065.355422.0&scm_id=1007.39065.355422.0&scm-url=1007.39065.355422.0&pvid=399d3826-8d67-4910-93bd-a8b96a744f69&utparam=%257B%2522process_id%2522%253A%2522standard-item-process-2%2522%252C%2522x_object_type%2522%253A%2522product%2522%252C%2522pvid%2522%253A%2522399d3826-8d67-4910-93bd-a8b96a744f69%2522%252C%2522belongs%2522%253A%255B%257B%2522floor_id%2522%253A%252240478212%2522%252C%2522id%2522%253A%252232680171%2522%252C%2522type%2522%253A%2522dataset%2522%257D%252C%257B%2522id_list%2522%253A%255B%25221000543522%2522%255D%252C%2522type%2522%253A%2522gbrain%2522%257D%255D%252C%2522pageSize%2522%253A%252218%2522%252C%2522language%2522%253A%2522es%2522%252C%2522scm%2522%253A%25221007.39065.355422.0%2522%252C%2522countryId%2522%253A%2522ES%2522%252C%2522scene%2522%253A%2522SD-Waterfall%2522%252C%2522tpp_buckets%2522%253A%252221669%25230%2523265320%25237_21669%25234190%252319165%2523787_29065%25230%2523355422%252310%2522%252C%2522x_object_id%2522%253A%25221005005878900854%2522%257D&pdp_npi=3%40dis%21EUR%21%E2%82%AC%203%2C64%21%E2%82%AC%200%2C99%21%21%21%21%21%40211b600e17038942960282114e0c4a%2112000035739136644%21gdf%21%21&aecmd=true")

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

#Devuelve como máximo 60 links
def get_url_products(description):

    #url = searchbar_format_Aliexpress(description)
    url = description
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    driver.implicitly_wait(8)

    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    actions = ActionChains(driver)

    for i in range(40):
        actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(3)
    link_elements = driver.find_elements(By.XPATH, "//a[@class='multi--container--1UZxxHY cards--card--3PJxwBm search-card-item']")

    link_hrefs = [element.get_attribute('href') for element in link_elements]

    print(link_hrefs)
    return

get_url_products("https://www.aliexpress.com/wholesale?catId=0&SearchText=Zoro")