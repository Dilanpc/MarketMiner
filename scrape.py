from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import datetime
import time
import pandas as pd
import csv_utils as csv

class ValueNotFoundByAttr(Exception):
    pass


# Clase que recibe un link y lo convierte en un objeto BeautifulSoup para facilitar la extracción de datos
class Page(BeautifulSoup):
    def __init__(self, link, use_selenium=False) -> None:
        self._driver = None
        if use_selenium:
            options = webdriver.chrome.options.Options()
            options.add_argument("--headless") # No abrir ventana de chrome
            options.add_argument('log-level=2') # No mostrar mensajes de log

            service = webdriver.chrome.service.Service(executable_path="./drivers/chromedriver.exe")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self._driver = webdriver.Chrome(service=service, options=options)
            self._driver.get(link)
            time.sleep(1)
            self.html = self._driver.page_source
            #### CONTENIDO DE PRUEBA
            with open("test.html", "w", encoding="utf-8") as file:
                file.write(self.html)
            ####
            self._driver.quit()

        else:
            self.html = requests.get(link).text

        super().__init__(self.html, 'lxml')



# Recibe un tag que continene la información de un producto para crear un objeto con los datos del procuto y facilitar su acceso
class ProductCard():
    def __init__(self, tag: BeautifulSoup, attrs_name:list[dict]=None, attrs_price:list[dict]=None, attrs_link:list[dict]=None, exc_attrs_name:dict=None, exc_attrs_price:dict=None, exc_attrs_link:dict=None) -> None:
        self.tag = tag
        self._attrs_name = attrs_name
        self._attrs_price = attrs_price
        self._attrs_link = attrs_link
        self._exc_attrs_name = exc_attrs_name
        self._exc_attrs_price = exc_attrs_price
        self._exc_attrs_link = exc_attrs_link
        self.name = ""
        self.price_txt = ""
        self.price = -1
        self.link = ""
        self.define_product()
    
    def define_product(self):
        self._compute_name()
        self._compute_price()
        self._compute_link()

    def _compute_name(self):
        if self._attrs_name == None:
            self.name = "Sin nombre"
            return self.name
        
        try:
            #Se busca el tag de siguiendo el orden de los atributos especificadas
            section:list[BeautifulSoup] = [self.tag]
            for attr in self._attrs_name:
                section = self._search_attrs_in_list(section, attr, self._exc_attrs_name)

            if len(section) > 1:
                raise ValueNotFoundByAttr("Se encontraron varios nombres")
            
            self.name = section[0].text
            return self.name
        except Exception as e:
            print(e, "No se pudo obtener el nombre")
            return ""
    
    def _compute_price(self):
        if self._attrs_price == None:
            self.price = "Sin precio"
            return self.price

        try:
            #Se busca el tag de siguiendo el orden de las clases especificadas
            section:list[BeautifulSoup] = [self.tag]
            for attr in self._attrs_price:
                section = self._search_attrs_in_list(section, attr, self._exc_attrs_price)

            if len(section) > 1:
                raise ValueNotFoundByAttr("Se encontraron varios precios")
            
            self.price_txt = section[0].text
            self.__decode_price()
            return self.price
        except Exception as e:
            print(e, "No se pudo obtener el precio")
            return -1

    def _compute_link(self):
        if self._attrs_link == None:
            self.link = "Sin link"
            return self.link
        
        try:
            #Se busca el tag de siguiendo el orden de las clases especificadas
            section:list[BeautifulSoup] = [self.tag]
            for attr in self._attrs_link:
                section = self._search_attrs_in_list(section, attr, self._exc_attrs_link)

            if len(section) > 1:
                print(section)
                raise ValueNotFoundByAttr("Se encontraron varios links")
            
            self.link = section[0].get('href')
            return self.name
        except Exception as e:
            print(e, "No se pudo obtener el link")
            return ""
        

    def _search_attrs_in_list(self, sections:list, attrs:dict, excluded:dict=None):
        
        # Obtener todos los tags con los atributos especificados en cada section
        result = []
        for i in range(len(sections)):
            result = result + sections[i].find_all(attrs=attrs)
            
        # Filtrar los tags que no contienen las clases excluidas
        filtered = []
        if excluded == None or excluded == {}:
            excluded = {}
            filtered = result
        for tag in result:
            # iterar en cada atributo excluido
            for exc in excluded:
                if exc not in tag.attrs or excluded[exc] not in tag[exc]:
                    filtered.append(tag)  # Si no se encuentra el atributo excluido, se agrega a la lista de tags filtrados

        if len(filtered) == 0:
            raise ValueNotFoundByAttr(f"No se encontró ningún tag con los atributos {attrs} y sin {excluded}")

        return filtered

    
    def __decode_price(self):
        self.price = ""
        for c in self.price_txt:
            if c.isdigit():
                self.price += c
        self.price = int(self.price)
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
    def __init__(self, use_selenium=False) -> None:
        self.page_name = ""
        self.link = ""
        self.products = []
        self.names = []
        self.prices = []
        self.links = []
        self.SELENIUM = use_selenium
        self._CARD_DATA = []  # Se incluyen las clases para istanciar los objetos ProductCard
    
    def _enter_webpage(self, link):
        self.link = link
        super().__init__(link, use_selenium=self.SELENIUM)

    def search_products(self, link: str):
        self._enter_webpage(link)
        self._compute_products()
        self._compute_info()

    def get_product_by_link(self, link: str):
        self._enter_webpage(link)
        return self._compute_one_product(link)

    def _compute_info(self):
        for product in self.products:
            self.prices.append(product.price)
            self.names.append(product.name)
            self.links.append(product.link)

    def _compute_products(self, *args): # Cada página tiene una estructura diferente, por lo que se debe sobreescribir
        pass
    def _compute_one_product(self, *args): # Cada página tiene una estructura diferente, por lo que se debe sobreescribir
        pass
    
    def make_report(self, file_name:str, link_file_name:str=None):
        # Crea un archivo csv con los productos encontrados
        file = csv.Csv(file_name)
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")

        if link_file_name != None:
            link_file = csv.Csv(link_file_name)

        if len(file) == 0:
            # Si el archivo está vacío, se crean los productos a rastrear
            matriz = [["Nombres", f"Precio {fecha_actual}"]] + [[name, price] for name, price in zip(self.names, self.prices)] # [[Nombres, fecha], [name1, precio1], [name2, precio2], ...]
            file.write(matriz)

            if link_file_name != None:
                link_file.write([["Nombres", f"Link {fecha_actual}"]] + [[name, link] for name, link in zip(self.names, self.links)])

        else:
            #Se agrega una nueva columna con los precios actuales
            column_names = file.get_column(0)
            column_to_add = [f"Precio {fecha_actual}"] + ["N/A"] * len(column_names)
            column_links = [f"link {fecha_actual}"] + ["N/A"] * len(column_names)
            #Se busca si los nombres de los productos que ya están en el archivo
            for i in range(1, len(column_names)): # Se inicia desde el segundo porque el primero es el nombre de la columna
                if column_names[i] in self.names:
                    index = self.names.index(column_names[i]) # Obtiene el índice del nombre en la lista de nombres
                    # Se ubica el precio y link en la misma posición que el nombre
                    column_to_add[i] = self.prices[index]
                    column_links[i] = self.links[index]
            
            # Escribir datos en el archivo
            file.add_column(column_to_add)
            if link_file_name != None:
                link_file.add_column(column_links)


    def print_products(self):
        if not self.products:
            print("No hay productos")
            return None
        
        #Buscar cadena más larga para ajustar el tamaño de la columna
        largest = len(self.products[0].name)
        for product in self.products:
            if len(product.name) > largest:
                largest = len(product.name)

        #Imprimir productos con precio
        for product in self.products:
            print(product.name + "."*(largest - len(product.name)), "->", product.price)
    
    def clean_up(self):
        self.products = []
        self.names = []
        self.prices = []
        self.links = []
        self.link = ""
    
    def average_price(self):
        return sum([int(product.price) for product in self.products]) / len(self.products)
    
    def get_dataframe(self):
        data = pd.DataFrame({"Nombres": self.names, "Precios": self.prices, "Links": self.links})
        return data
    
    def get_dataframe_report(self, file_name:str):
        file = csv.Csv(file_name)
        return file.get_dataframe()


class MercadoLibre(Products):
    def __init__(self) -> None:
        super().__init__(use_selenium=False)
        self.page_name = "MercadoLibre"
        self.__CARD_DATA = [
            [{"class":"ui-search-item__title"}], # Atributos para nombre
            [{"class":"ui-search-price ui-search-price--size-medium"},{"class":"andes-money-amount"}], # Atributos para precio
            [{"class":"ui-search-item__group__element ui-search-link__title-card ui-search-link"}], # Atribitos para link
            {}, # Atributos excluidos para nombre
            {"class":"ui-search-price__original-value"}, # Atributos excluidos para precio
            {} # Atributos excluidos para link
        ]


    def search_products(self, product: str):
        super().search_products(f"https://listado.mercadolibre.com.co/{product}")

    def get_product_by_link(self, link: str):
        return super().get_product_by_link(link)
    
    def _compute_one_product(self, link):
        section = self.find(class_="ui-pdp-container__col col-2 mr-32")
        ATTR_NAME = [{"class":"ui-pdp-title"}]
        ATTR_PRICE = [{"class":"ui-pdp-price__main-container"}, {"class":"andes-money-amount--cents-superscript"}, {"class":"andes-money-amount__fraction"}]
        EXCLUDED_ATTR_PRICE = {"class":"ui-pdp-price__original-value"}
        product = ProductCard(section, ATTR_NAME, ATTR_PRICE, exc_attrs_price=EXCLUDED_ATTR_PRICE)
        product.link = link
        return product

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




class Exito(Products):
    def __init__(self):
        super().__init__(use_selenium=True)
        self.page_name = "Exito"
        self._CARD_DATA = [
            [{"data-fs-product-card-title":"true"}], # Atributos para nombre
            [{"class":"ProductPrice_container__price__XmMWA"}], # Atributos para precio
            [{"data-fs-product-card-title":"true"}, {"data-testid":"product-link"}], # Atributos para link
            {}, # Atributos excluidos para nombre
            {}, # Atributos excluidos para precio
            {}  # Atributos excluidos para link
        ]
        self._CARD_DATA2 = [
            [{"class":"styles_name__qQJiK"}], # Atributos para nombre
            [{"class":"ProductPrice_container__price__XmMWA"}], # Atributos para precio
            [{"class":"productCard_productLinkInfo__It3J2"}], # Atributos para link
            {}, # Atributos excluidos para nombre
            {}, # Atributos excluidos para precio
            {}  # Atributos excluidos para link
        ]

    def search_products(self, product: str):
        super().search_products(f"https://www.exito.com/s?q={product}")

    def _compute_products(self):
        try:
            product_section: BeautifulSoup = self.find(class_="product-grid_fs-product-grid___qKN2")
            card_list = product_section.find_all(attrs={"class":"productCard_contentInfo__CBBA7 productCard_column__Lp3OF"})
            

            for card in card_list: #Convierte todos los tags en objetos ProductCard
                self.products.append(ProductCard(card, *self._CARD_DATA2))
                self.products[-1].link = "https://www.exito.com" + self.products[-1].link

            return self.products

        except Exception as e:
            print(e, "No se encontraron productos")
            return None
    





if __name__ == "__main__":
    page = Exito()
    page.search_products(input("Producto: "))
    page.print_products()