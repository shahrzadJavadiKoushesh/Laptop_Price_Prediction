import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko + '.exe')
driver.get("https://torob.com/search/?query=%D9%84%D9%BE%20%D8%AA%D8%A7%D9%BE")

for i in range(100):
    driver.execute_script("window.scrollBy(0, -500);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    print(i, end=" ")

laptop_names = []
prices = []
RAMs = []
CPUs = []
wait = WebDriverWait(driver, 10)
laptops = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, "/html/body/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div")))

for laptop in laptops:
    name = laptop.find_element(By.XPATH, "./a/div/div/h2").text
    laptop_names.append(name)
    # RAM info
    if name.__contains__("GB"):
        ram = name.find("GB")
        ram_capacity = name[ram - 2] + name[ram - 1]
        if ram_capacity.isdigit() or any((char.isspace() and any(char.isdigit() for char in ram_capacity)) or (
            char.isdigit() and any(char.isspace() for char in ram_capacity)) for char in ram_capacity):
            RAMs.append(int(ram_capacity))
    # CPU info
    if name.__contains__(" i") or name.__contains__(" I"):
        cpu = name.find(" i")
        cpu_capacity = name[cpu+2]
        CPUs.append("i"+str(cpu_capacity))
    else:
        RAMs.append("?")
        CPUs.append("?")
    prices.append(laptop.find_element(By.XPATH, "./a/div/div/div[2]/div[2]").text)

for i in range(len(laptop_names)):
    print("laptop " + str(i) + ":" + laptop_names[i] + " " + prices[i])
    print("RAM" + str(i) + ":" + str(RAMs[i]))
    print("CPU" + str(i) + ":" + str(CPUs[i]))
