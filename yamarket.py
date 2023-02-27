# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import json
import re

import undetected_chromedriver as uc


def scroll_the_page(driver):

    scroll_counter = 0

    while len(driver.find_elements(By.TAG_NAME, "article")) < 48 and scroll_counter < 30:

        element = driver.find_element(By.XPATH, "//main[@id='searchResults'][@aria-label='Результаты поиска']")
        driver.execute_script("scrollBy({top: 250, behavior: 'smooth'})", element)
        
        # data = driver.find_elements(By.XPATH, "//article[@data-auto='product-snippet']")

        data = driver.find_elements(By.TAG_NAME, "article")
        
        print(f'{len(data)} items found on page')

        scroll_counter += 1

        time.sleep(2)


# the function isn't used    
def click_forward_button(driver):

    element = driver.find_element(By.XPATH, "//button[@data-auto='pager-more']")
    element.send_keys(Keys.ENTER)
    element.click()


def process_the_page(driver, finished):

    index = len(finished)

    # data = driver.find_elements(By.XPATH, "//article[@data-auto='product-snippet']")
    data = driver.find_elements(By.TAG_NAME, "article")

    for item in data:

        soup = BeautifulSoup(item.get_attribute("outerHTML"), 'html.parser')
        js = json.loads(soup.article['data-zone-data'])
        
        try:
            price = js['price']
        except KeyError:
            return 'no_price_item' #end the function if the items with the price are over 
        
        try:
            old_price = js['oldPrice']
        except KeyError:
            old_price = js['price']

        sku_id = js['skuId']
        warehouse_id = js['warehouseId']

        try:
            link = f"https://market.yandex.ru{soup.a['href']}"
            img = soup.a.div.img['src']
            title = soup.a.div.img['title']
        except AttributeError:
            link = f"https://market.yandex.ru{soup.h3.a['href']}"
            img = soup.img['src']
            title = soup.h3.a['title']
        
        rating_block = soup.find('div', attrs={'data-auto': 'product-rating'})
        if rating_block:
            spans = rating_block.find_all('span')

            if len(spans) == 4:
                rating = float(spans[1].string)
                feedback_count = int(re.sub('\D', '', spans[3].string))
        
            elif len(spans) == 1:
                rating = 0
                feedback_count = int(re.sub('\D', '', spans[0].string))
        else:
            rating = 0
            feedback_count = 0


        finished.append(
            {
                'index': index,
                'sku_id': sku_id,
                'price': price,
                'old_price': old_price,
                'warehouse_id': warehouse_id,
                'link': link,
                'img': img,
                'title': title,
                'rating': rating,
                'feedback_count': feedback_count
            }
        )

        index += 1        


def check_url(driver):

    if re.search('https://market.yandex.ru/showcaptcha', driver.current_url):
        
        time.sleep(40) # time to enter the captcha



def main():

    url = 'https://market.yandex.ru'
    finished = []
    page = 1

    # driver = webdriver.Chrome('chromedriver.exe')
    # driver = webdriver.Firefox()
    driver = uc.Chrome()
    driver.maximize_window()
    driver.get(url)

    time.sleep(10)

    check_url(driver)

    time.sleep(10)

    search_line = driver.find_element(By.ID, "header-search")
    search_line.send_keys('Термопаста', Keys.ENTER)

    time.sleep(10)

    check_url(driver)

    scroll_the_page(driver)
    process_the_page(driver, finished)

    while page < 20:  #20
        
        page += 1
        page_number = f'&page={page}'

        time.sleep(10)

        driver.get(driver.current_url + page_number)
        
        time.sleep(10)

        check_url(driver)
    
        print(f'Page {page} in process...')
    
        scroll_the_page(driver)
        
        if process_the_page(driver, finished) == 'no_price_item':

            with open('finished.json', 'w') as products:
                products.write(json.dumps(finished))

            print('The script has been completed.')
            
            return # end the scritp if the items with the price are over
    
        print(f'Added {len(finished)} elements')
        print('------------------------------------')

    with open('finished.json', 'w') as products:
        products.write(json.dumps(finished))

    print('The script has been completed.')


if __name__ == "__main__":
    main()


