import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook

from cian import cian_check, get_chrome_service

pages = list(range(3))
cian_times = 15
saved = []
avito_page = 'https://www.avito.ru/moskva/kvartiry/prodam/vtorichka-ASgBAgICAkSSA8YQ5geMUg?context=&f=ASgBAQECBESSA8YQ5geMUpC~DZauNcDBDbr9NwFAyggkglmAWQFFxpoMH3siZnJvbSI6MTAwMDAwMDAsInRvIjoyMDAwMDAwMH0&localPriority=0&metro=88'
cian_page = 'https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&maxprice=20000000&metro%5B0%5D=94&minprice=10000000&object_type%5B0%5D=1&offer_type=flat&p=4&room1=1&room2=1'

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


wb = Workbook()
ws = wb.active
ws.append(["№", "Адрес", "Город", "Кол-во комнат", "Площадь (м²)", "Этаж", "Цена (₽)", "Цена за м² (₽)", "Дата", "Ссылка", "Циан"])

cian_checked = cian_check(cian_times, cian_page)

for page in pages:
    dct = cian_checked
    print(cian_checked)

    driver = webdriver.Chrome(service=get_chrome_service(), options=options)
    driver.get(avito_page + "&p=" + str(page + 1))

    driver.execute_script("""
        var elements = document.getElementsByClassName('items-witcher-FjJnZ');
        while (elements.length > 0) {
            elements[0].parentNode.removeChild(elements[0]);
        }
    """)


    items = driver.find_elements(By.CLASS_NAME, "iva-item-root-Se7z4")
    main = driver.find_elements(By.CLASS_NAME, "iva-item-titleStep-zichc")
    price = driver.find_elements(By.CLASS_NAME, "price-root-IfnJI")
    date = driver.find_elements(By.CLASS_NAME, "iva-item-dateInfoStep-qcDJA")
    geo = driver.find_elements(By.CLASS_NAME, "geo-root-NrkbV")
    links = driver.find_elements("css selector", "[data-marker='item-title']")
    print(len(main), len(price), len(date), len(geo), len(links), links[0].get_attribute('href'))

    for q in range(len(main)):
            if 'Сегодня' in date[q].text or 'Вчера' in date[q].text or "неделю" in date[q].text or "час" in date[q].text or "дн" in date[q].text :
                if price[q].text.split('₽')[1] not in saved:
                    rooms, area, floor = main[q].text.split(", ")[:3]
                    address = geo[q].text
                    city = "Москва, Планерная"
                    price_full = price[q].text.split('₽')[0]
                    price_per_m2 = price[q].text.split('₽')[1]
                    link = links[q].get_attribute('href')
                    cian = 'НЕТ'
                    
                    price_per_m2 = price_per_m2.replace(' ', '').replace('\n', '')
                    print(price_per_m2)
                    
                    if price_per_m2.replace(' ', '').replace('\n', '') in dct:
                        cian = dct[price_per_m2]
                    ws.append([count, address, city, rooms, area, floor, price_full, price_per_m2.strip(), date[q].text, link, cian])
                    print(price_per_m2)
                    count += 1
                    saved.append(price[q].text.split('₽')[1])
    driver.quit()


file_path = os.path.join(os.path.dirname(__file__), "10-20 Москва, Планерная.xlsx")
wb.save(file_path)

print(f"Данные сохранены в {file_path}")
