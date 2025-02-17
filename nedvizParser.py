import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

pages = list(range(2))
saved = []
# Настройки Chrome
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

count = 1

# Настройка сервиса ChromeDriver
def get_chrome_service():
    return Service(
        executable_path=r"C:\\Users\\Acer\\Desktop\\PaketSPaketami\\parser\\chromedriver.exe",
        log_path=os.devnull
    )

# Создание Excel-файла
wb = Workbook()
ws = wb.active
ws.append(["№", "Адрес", "Город", "Кол-во комнат", "Площадь (м²)", "Этаж", "Цена (₽)", "Цена за м² (₽)", "Дата", "Ссылка"])

for page in pages:
        
    # Открытие браузера
    driver = webdriver.Chrome(service=get_chrome_service(), options=options)
    driver.get("https://www.avito.ru/himki/kvartiry/prodam/do-15-mln-rubley-ASgBAgECAUSSA8YQAUXGmgwYeyJmcm9tIjowLCJ0byI6MTUwMDAwMDB9?context=H4sIAAAAAAAA_wEtANL_YToxOntzOjg6ImZyb21QYWdlIjtzOjE2OiJzZWFyY2hGb3JtV2lkZ2V0Ijt9F_yIfi0AAAA&f=ASgBAgECAkSSA8YQygiCWQFFxpoMGHsiZnJvbSI6MCwidG8iOjE1MDAwMDAwfQ&p="+str(page + 1))

    # Ожидание загрузки элементов
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "iva-item-root-Se7z4"))
    )

    # Удаление элементов с классом items-witcher-FjJnZ
    driver.execute_script("""
        var elements = document.getElementsByClassName('items-witcher-FjJnZ');
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }
    """)

    # Поиск всех элементов
    items = driver.find_elements(By.CLASS_NAME, "iva-item-root-Se7z4")
    main = driver.find_elements(By.CLASS_NAME, "iva-item-titleStep-zichc")
    price = driver.find_elements(By.CLASS_NAME, "price-root-IfnJI")
    date = driver.find_elements(By.CLASS_NAME, "iva-item-dateInfoStep-qcDJA")
    geo = driver.find_elements(By.CLASS_NAME, "geo-root-NrkbV")
    links = [i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in items]
    print(len(items))

    # Запись данных в Excel
    for q in range(len(items) - 1):
            if 'Сегодня' in date[q].text or 'Вчера' in date[q].text or "недел" in date[q].text or "час" in date[q].text or "дн" in date[q].text :
                if price[q].text.split('₽')[1] not in saved:
                    rooms, area, floor = main[q].text.split(", ")[:3]
                    address = geo[q].text
                    city = "Химки"  # Указать город
                    price_full = price[q].text.split('₽')[0]
                    price_per_m2 = price[q].text.split('₽')[1]
                    link = links[q]
                    ws.append([count, address, city, rooms, area, floor, price_full, price_per_m2, date[q].text, link])
                    print(price_per_m2)
                    count += 1
                    saved.append(price[q].text.split('₽')[1])
    driver.quit()

# Сохранение файла в той же директории, что и скрипт
file_path = os.path.join(os.path.dirname(__file__), "test5.xlsx")
wb.save(file_path)

print(f"Данные сохранены в {file_path}")
