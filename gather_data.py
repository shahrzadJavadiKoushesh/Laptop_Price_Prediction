import requests
from bs4 import BeautifulSoup

# create a requests session
session = requests.Session()

# make a GET request to the Torob website search page for "لپ تاپ"
response = session.get("https://torob.com/search/?query=%D9%84%D9%BE%20%D8%AA%D8%A7%D9%BE")

# create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, "html.parser")

# find all the laptop elements on the page
laptop_elements = soup.find_all("div", attrs={"class": "jsx-fa8eb4b3b47a1d18"})

# loop through the laptop elements and extract the information
for i, laptop in enumerate(laptop_elements[:1000]):
    
    #  get the laptop price
    price = laptop.find("div", attrs={"class": "jsx-fa8eb4b3b47a1d18"})
    
    # get the laptop name
    name = laptop.find("h2", attrs={"class": "jsx-fa8eb4b3b47a1d18 name"})
    
    # print the laptop information
    print(f"Laptop {i}: {name} - {price}")
print(len(laptop_elements))