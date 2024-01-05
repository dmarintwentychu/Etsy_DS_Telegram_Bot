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
    

    def __init__(self, url):
        self.url = url
                
        options = webdriver.ChromeOptions()
        options.add_argument('---incognito')
        options.add_argument('--disable-gpu')
        #options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)

        wait = WebDriverWait(self.driver, 10)
        block = True
        while(block):
            try:
                self.driver.get(self.url)
                self.driver.minimize_window()
                self.driver.implicitly_wait(4)
                self.driver.refresh()
                self.driver.implicitly_wait(10)
                boton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='wt-btn wt-btn--filled wt-mb-xs-0']")))
                boton.click()
                block = False
            except TimeoutException:
                print("No hay boton(?)")

        self.is_hand_made()
        self.search_price()
        self.search_Shipping_Costs()
        self.totalPriece = self.price + self.shippingCosts
        self.search_rating()
        self.search_nReviews()
        self.search_nShopRating()
        self.search_description()
        self.download_img_etsy()

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
            reviews_elem = self.driver.find_element(By.XPATH,'//div[@class="wt-display-flex-xs wt-align-items-center"]')
            self.nShopRating = int(reviews_elem.text.split()[0])
        except:
            self.nShopRating = False

    def search_description(self):

        self.description = self.driver.find_elements(By.XPATH,'//div[@class="wt-mb-xs-1"]/h1[@class="wt-text-body-01 wt-line-height-tight wt-break-word wt-mt-xs-1"]')[0].text

    def download_img_etsy(self):

        imagenes = self.driver.find_elements(By.XPATH, '//div[@id="photos"]//img')

        urls_imagenes = [imagen.get_attribute("src") for imagen in imagenes]

        i = 0
        for url in urls_imagenes:
            urllib.request.urlretrieve(url, f'./imgcacheetsy/img{i}.jpg')
            i += 1

        self.imgs = len(urls_imagenes)