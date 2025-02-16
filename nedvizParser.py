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
pages = ['', 'p=2', 'p=3']
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

# Настройка сервиса ChromeDriver
def get_chrome_service():
    return Service(
        executable_path=r"C:\\Users\\Acer\\Desktop\\PaketSPaketami\\parser\\chromedriver.exe",
        log_path=os.devnull
    )
# Создание Excel-файла
wb = Workbook()
ws = wb.active
ws.append(["Адрес", "Город", "Кол-во комнат", "Площадь (м²)", "Этаж", "Цена (₽)", "Цена за м² (₽)", "Дата", "Ссылка"])
for i in range(3):
        
    # Открытие браузера
    driver = webdriver.Chrome(service=get_chrome_service(), options=options)
    driver.get("https://www.avito.ru/himki/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_wEkANv_YToxOntzOjg6ImZyb21QYWdlIjtzOjg6InZlcnRpY2FsIjt938025iQAAAA&f=ASgBAQECBUSSA8YQ5geMUpC~DZauNay~DaTHNcDBDbr9NwJAyggkgFn~WOzBDTSGzzmEzzmCzzkBRcaaDBh7ImZyb20iOjAsInRvIjoxMDAwMDAwMH0&"+pages[i])

    # Ожидание загрузки элементов
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "iva-item-root-Se7z4"))
    )

    # Поиск всех элементов
    items = driver.find_elements(By.CLASS_NAME, "iva-item-root-Se7z4")
    main = driver.find_elements(By.CLASS_NAME, "iva-item-titleStep-zichc")
    price = driver.find_elements(By.CLASS_NAME, "price-root-IfnJI")
    date = driver.find_elements(By.CLASS_NAME, "iva-item-dateInfoStep-qcDJA")
    geo = driver.find_elements(By.CLASS_NAME, "geo-root-NrkbV")
    links = [i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in items]


    # Запись данных в Excel
    for i in range(len(items) - 1):
        try:
            if 'Сегодня' in date[i].text or 'Вчера' in date[i].text or "недел" in date[i].text:
                rooms, area, floor = main[i].text.split(", ")[:3]
                address = geo[i].text
                city = "Химки"  # Указать город
                price_full = price[i].text.split('₽')[0]
                price_per_m2 = price[i].text.split('₽')[1]
                link = links[i]
                ws.append([address, city, rooms, area, floor, price_full, price_per_m2, date[i].text, link])
        except Exception as e:
            print(f"Ошибка обработки данных: {e}")
    driver.quit()
# Сохранение файла в той же директории, что и скрипт
file_path = os.path.join(os.path.dirname(__file__), "avito_data3.xlsx")
wb.save(file_path)

print(f"Данные сохранены в {file_path}")
