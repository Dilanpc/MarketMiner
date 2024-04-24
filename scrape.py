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
    def __init__(self, tag: BeautifulSoup) -> None:
        self.tag = tag
        self.define_product()
    
    def define_product(self):
        self.get_name()
        self.get_price()
        self.get_link()

    def get_name(self):
        try:
            self.name = self.tag.find(class_="ui-search-item__title").text
            return self.name
        except AttributeError:
            return None
    
    def get_price(self):
        try:
            self.price = self.tag.find(class_="andes-money-amount__fraction").text
            return self.price
        except AttributeError:
            return None
    
    def get_link(self):
        try:
            self.link = self.tag.find(class_="ui-search-link").get("href")
            return self.link
        except AttributeError:
            return None
    
        



# pensado para obtener los productos de MercadoLibre por ahora
class Products(Page):
    def __init__(self, link="https://www.mercadolibre.com.co/") -> None:
        super().__init__(link)
        self.page_name = "MercadoLibre"
        self.products = []
    
    def search_product(self, product: str):
        self.product = product
        self.link = f"https://listado.mercadolibre.com.co/{product}"
        super().__init__(self.link)
        self.get_products()

    def get_products(self):
        try:
            product_section: BeautifulSoup = self.find(class_="ui-search-layout")
            card_list = product_section.find_all(class_="ui-search-layout__item")

            for card in card_list: #Convierte todos los tags en objetos ProductCard
                self.products.append(ProductCard(card))

            return self.products

        except Exception as e:
            print(e, "No se encontraron productos")
            return None
        
    def print_products(self):
        for product in self.products:
            print(product.name, "->", product.price)
        



if __name__ == "__main__":
    page = Products()

    page.search_product("computadores")
    page.print_products()