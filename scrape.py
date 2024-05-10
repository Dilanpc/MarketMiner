from bs4 import BeautifulSoup
import requests


    
def clear_text(text: str):
    for i in range(len(text)):
        if text[-i-1] == '\r':
            return text[:-i-1][1:]
    return text

class Page(BeautifulSoup):
    def __init__(self, link) -> None:
        self.html = requests.get(link).text
        super().__init__(self.html, 'lxml')



# Recibe un tag que continene la información de un producto para crear un objeto con los datos del procuto y facilitar su acceso
class ProductCard():
    def __init__(self, tag: BeautifulSoup, class_name, class_price, class_link) -> None:
        self.tag = tag
        self._class_name = class_name
        self._class_price = class_price
        self._class_link = class_link
        self.define_product()
    
    def define_product(self):
        self._compute_name()
        self._compute_price()
        self._compute_link()

    def _compute_name(self):
        try:
            self.name = self.tag.find(class_=self._class_name).text
            return self.name
        except AttributeError:
            return None
    
    def _compute_price(self):
        try:
            self.price_txt = self.tag.find(class_=self._class_price).text
            self._decode_price()
            return self.price
        except AttributeError:
            print("No se encontró el precio")
            return None

    def _compute_link(self):
        try:
            self.link = self.tag.find(class_=self._class_link).get("href")
            return self.link
        except AttributeError:
            return None
    
    def _decode_price(self):
        self.price = int(self.price_txt.replace(".", ""))
        return self.price
    
    #Getters
    def get_name(self):
        return self.name
    def get_price(self):
        return self.price
    def get_link(self):
        return self.link
    
    def __str__(self) -> str:
        return f"{self.name} -> {self.price}"
        


class Products(Page):
    def __init__(self) -> None:
        self.page_name = ""
        self.link = ""
        self.products = []
        self.names = []
        self.prices = []
        self.links = []
    
    def search_product(self, link: str):
        self.link = link
        super().__init__(self.link)
        self._compute_products()
        self._compute_info()

    def _compute_info(self):
        for product in self.products:
            self.prices.append(product.price)
            self.names.append(product.name)
            self.links.append(product.link)

    def _compute_products(self): # Cada página tiene una estructura diferente, por lo que se debe sobreescribir
        pass
    
    def print_products(self):
        if not self.products:
            print("No se encontraron productos")
            return None
        
        #Buscar cadena más larga para ajustar el tamaño de la columna
        largest = len(self.products[0].name)
        for product in self.products:
            if len(product.name) > largest:
                largest = len(product.name)

        #Imprimir productos con precio
        for product in self.products:
            print(product.name + "."*(largest - len(product.name)), "->", product.price)

    
    def average_price(self):
        return sum([int(product.price) for product in self.products]) / len(self.products)
    


class MercadoLibre(Products):
    def __init__(self) -> None:
        super().__init__()
        self.page_name = "MercadoLibre"
        self.__CARD_DATA = ["ui-search-item__title", "andes-money-amount__fraction", "ui-search-link"]


    def search_product(self, product: str):
        super().search_product(f"https://listado.mercadolibre.com.co/{product}")

    def _compute_products(self):
        try:
            product_section: BeautifulSoup = self.find(class_="ui-search-layout")
            card_list = product_section.find_all(class_="ui-search-layout__item")

            for card in card_list: #Convierte todos los tags en objetos ProductCard
                self.products.append(ProductCard(card, *self.__CARD_DATA))

            return self.products

        except Exception as e:
            print(e, "No se encontraron productos")
            return None















if __name__ == "__main__":
    page = MercadoLibre()

    page.search_product("iphone 15")
    page.print_products()
    print("Promedio: ", page.average_price())

    maximo = page.products[0]
    for product in page.products:
        if product.price > maximo.price:
            maximo = product

    print(maximo)
    print(maximo.link)