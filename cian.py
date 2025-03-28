import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

saved = []

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-logging")
options.add_argument("--disable-infobars")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option("useAutomationExtension", False)


def get_chrome_service():
    return Service(
        executable_path=r"C:\\Users\\Acer\\Desktop\\PaketSPaketami\\parser\\chromedriver.exe",
        log_path=os.devnull
    )

def cian_check(links, page_example):
    page_list = list()
    for link in range(1, links + 1):
        p_index = page_example.find("p=")
        if p_index != -1:
            p_end_index = page_example.find("&", p_index)
            if p_end_index == -1:
                p_end_index = len(page_example)
            
            current_page = page_example[:p_index + 2] + str(link) + page_example[p_end_index:]
        else:
            current_page = page_example + "&p=" + str(link)
        
        print(current_page)
        page_list.append(current_page)
        
    result = {}

    for page in page_list:
        driver = webdriver.Chrome(service=get_chrome_service(), options=options)
        driver.get(page)

        driver.implicitly_wait(10)

        prices = driver.find_elements(By.CLASS_NAME, "_93444fe79c--container--aWzpE")
        prices = [price.text for price in prices if '₽/м²' in price.text]
        prices = [price[:price.find(' ₽')].replace(' ', '').replace('\n', '') for price in prices]

        links = driver.find_elements(By.CSS_SELECTOR, "a._93444fe79c--link--VtWj6")
        links = [link.get_attribute('href') for link in links]

        dct = {prices[i]: links[i] for i in range(len(links))}

        result = {**result, **dct}
        print('CIAN', prices[0], len(prices[0]))

        driver.quit()

    return result

