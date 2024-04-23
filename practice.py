from bs4 import BeautifulSoup
import requests


#Scraping de un archivo local

# with open('index.html', 'r') as file:
#     content = file.read()
    
#     soup = BeautifulSoup(content, 'lxml')
#     tags = soup.find_all(class_="product")

#     prices: list = []
#     names: list = []
#     for tag in tags:
#         title = tag.h2
#         price = tag.find(class_="price")
#         print(title.text, "->", price.text)

class Page(BeautifulSoup):
    def __init__(self, link) -> None:
        self.html = requests.get(link).text
        super().__init__(self.html, 'lxml')



page = Page("https://scrapepark.org/")

# Obteniedo lista de productos
product_section = page.find(class_="product-section")
product = product_section.find_all(class_="detail-box")
data_products = []

for i in range(len(product)): #quitar saltos de línea y espacios innecesarios
    for j in range(len(product[i].h5.text)):
        if product[i].h5.text[-j-1] == '\r':
            txt = product[i].h5.text
            data_products.append(txt[:-j-1][1:])
            print(data_products[-1])
            break


# Obteniendo lista de precios
prices = product_section.find_all('h6')
data_prices = []

for price in prices:
    txt = price.text.replace(' ', '')
    txt = txt[:-2][2:]
    print(txt)
    data_prices.append(int(txt[1:]))

print("\nPromedio de precios:")
print('$' + str(sum(data_prices)/len(data_prices)))


#Producto y precio
for i in range(len(product)):
    print(data_products[i], "->", data_prices[i])