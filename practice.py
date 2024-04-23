from bs4 import BeautifulSoup


with open('index.html', 'r') as file:
    content = file.read()
    
    soup = BeautifulSoup(content, 'lxml')
    tags = soup.find_all(class_="product")

    prices: list = []
    names: list = []
    for tag in tags:
        title = tag.h2
        price = tag.find(class_="price")
        print(title.text, "->", price.text)

