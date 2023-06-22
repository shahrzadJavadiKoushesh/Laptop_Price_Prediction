import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
import json

gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko + '.exe')
driver.get("https://torob.com/browse/99/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-%D9%88-%D9%86%D9%88%D8%AA-%D8%A8%D9%88%DA%A9-laptop/?stock_status=new")

file = open('data.csv', 'w')
file.close()

for i in range(250):
    driver.execute_script("window.scrollBy(0, -500);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    print(i, end=" ")

data = []
wait = WebDriverWait(driver, 10)
laptops = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, "/html/body/div/div/div/div/div/div[2]/div/div[2]/div[2]/div[3]/div/div/div")))

links = [laptop.find_element(By.XPATH, "./a").get_attribute("href").split("/")[4] for laptop in laptops]
responses = map(lambda href: requests.get(f"https://api.torob.com/v4/base-product/details-log-click/?prk={href}"), links)

for response in responses:
    json_data = json.loads(response.text)
    laptop = json_data["attributes"]
    price = json_data["price"]
    laptop["price"] = price
    data.append(laptop)

data_dict = {"cpu": [d.get("cpu") for d in data],
             "hdd": [d.get("hdd") for d in data],
             "ram": [d.get("ram") for d in data],
             "ssd": [d.get("ssd") for d in data],
             "graphic_ram": [d.get("graphic_ram") for d in data],
             "screen_size": [d.get("screen_size") for d in data],
             "stock_status": [d.get("stock_status") for d in data],
             "price": [d.get("price") for d in data]}

df = pd.DataFrame(data_dict)
df.to_csv("data.csv", index=False)
