import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko + '.exe')
driver.get("https://torob.com/search/?query=%D9%84%D9%BE%20%D8%AA%D8%A7%D9%BE")

lap_top_names = []
prices = []
laptops = driver.find_elements(By.XPATH, "/html/body/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div")

for laptop in laptops:
    lap_top_names.append(laptop.find_element(By.XPATH, "./a/div/div/h2").text)
    prices.append(laptop.find_element(By.XPATH, "./a/div/div/div[2]/div[2]").text)

for i in range(len(lap_top_names)):
    print("laptop" + str(i+1) + ":" + lap_top_names[i] + " " + prices[i])
    print()