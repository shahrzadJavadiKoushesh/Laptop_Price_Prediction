import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests

gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko + '.exe')
driver.get("https://torob.com/search/?query=%D9%84%D9%BE%20%D8%AA%D8%A7%D9%BE")

file = open('data.csv', 'w')
file.close()

for i in range(200):
    driver.execute_script("window.scrollBy(0, -500);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    print(i, end=" ")

data = []
wait = WebDriverWait(driver, 10)
laptops = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, "/html/body/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div")))

for laptop in laptops:
    link = laptop.find_element(By.XPATH, "./a")
    href = link.get_attribute("href").split("/")[4]
    url = f"https://api.torob.com/v4/base-product/details-log-click/?prk={href}"
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
        price = json.get("price")
        attributes = json.get("attributes")
        if price and attributes:
            attributes["price"] = price
            data.append(attributes)

data_dict = {
    "cpu": [],
    "hdd": [],
    "ram": [],
    "ssd": [],
    "graphic_ram": [],
    "screen_size": [],
    "stock_status": [],
    "price": []
}

for laptop in data:
    for key in data_dict:
        data_dict[key].append(laptop.get(key))

df = pd.DataFrame(data_dict)
df.to_csv("data.csv", index=False)
print(df.shape)
